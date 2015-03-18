from zope.interface import implementer
from pyramid.decorator import reify
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import (
    IdNameDescriptionMixin, Value, Unit, Parameter, Source, Contributor,
)


class Domain(Base, IdNameDescriptionMixin):
    pass


class Subdomain(Base, IdNameDescriptionMixin):
    domain_pk = Column(Integer, ForeignKey('domain.pk'))
    domain = relationship(Domain, backref='subdomains')


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.IParameter)
class Concept(CustomModelMixin, Parameter):
    """one row in what used to be the word-meaning association table
    """
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)

    ref = Column(Integer, nullable=False, unique=True)
    core = Column(Boolean, nullable=False)
    subdomain_pk = Column(Integer, ForeignKey('subdomain.pk'))
    subdomain = relationship(Subdomain, backref='concepts')

    ff = Column(Boolean, default=False)
    species = Column(Unicode)
    family = Column(Unicode)

    @reify
    def thumbnail(self):
        for f in self._files:
            if f.mime_type.startswith('image'):
                return self._files[0]

    @reify
    def video(self):
        for f in self._files:
            if f.mime_type.startswith('video'):
                return self._files[0]

    @property
    def eol_url(self):
        eol_id = self.jsondata.get('eol_id')
        if eol_id:
            return 'http://eol.org/%s' % eol_id


@implementer(interfaces.IValue)
class Counterpart(CustomModelMixin, Value):
    """one row in what used to be the word-meaning association table
    """
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)

    comment = Column(Unicode)
    unit_pk = Column(Integer, ForeignKey('unit.pk'))
    unit = relationship(Unit, backref='counterparts')


@implementer(interfaces.ISource)
class Document(CustomModelMixin, Source):
    pk = Column(Integer, ForeignKey('source.pk'), primary_key=True)

    # project docs will have an associated file!
    project_doc = Column(Boolean)

    contributors = association_proxy('contributor_assocs', 'contributor')


class DocumentContributor(Base):
    document_pk = Column(Integer, ForeignKey('document.pk'))
    contributor_pk = Column(Integer, ForeignKey('contributor.pk'))

    # contributors are ordered.
    ord = Column(Integer, default=0)

    document = relationship(Document, backref='contributor_assocs')
    contributor = relationship(Contributor, lazy=False, backref='document_assocs')
