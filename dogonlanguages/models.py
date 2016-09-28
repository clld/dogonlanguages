from __future__ import print_function, division, unicode_literals

from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    Float,
    CheckConstraint,
    Date,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import (
    IdNameDescriptionMixin, Value, Unit, Parameter, Source, Contributor, Language,
    FilesMixin, HasFilesMixin,
)

from dogonlanguages.interfaces import IVillage, IFile


class Domain(Base, IdNameDescriptionMixin):
    pass


class Subdomain(Base, IdNameDescriptionMixin):
    domain_pk = Column(Integer, ForeignKey('domain.pk'))
    domain = relationship(Domain, backref='subdomains')


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class Languoid(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    in_project = Column(Boolean, default=True)
    family = Column(Unicode)


@implementer(interfaces.IContributor)
class Member(CustomModelMixin, Contributor):
    pk = Column(Integer, ForeignKey('contributor.pk'), primary_key=True)
    abbr = Column(Unicode)


@implementer(interfaces.IParameter)
class Concept(CustomModelMixin, Parameter):
    """one row in what used to be the word-meaning association table
    """
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)

    core = Column(Boolean, nullable=False)
    subdomain_pk = Column(Integer, ForeignKey('subdomain.pk'))
    subdomain = relationship(Subdomain, backref='concepts')

    ff = Column(Boolean, default=False)
    species = Column(Unicode)
    family = Column(Unicode)
    tsammalex_taxon = Column(Unicode)

    count_videos = Column(Integer, default=0)
    count_images = Column(Integer, default=0)

    @property
    def videos(self):
        return [f for f in self._files if f.mime_type.startswith('video')]

    @property
    def images(self):
        return [f for f in self._files if f.mime_type.startswith('image')]

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


class LatLonMixin(object):
    latitude = Column(
        Float(),
        CheckConstraint('-90 <= latitude and latitude <= 90'),
        doc='geographical latitude in WGS84')
    longitude = Column(
        Float(),
        CheckConstraint('-180 <= longitude and longitude <= 180 '),
        doc='geographical longitude in WGS84')


class Village_files(Base, FilesMixin, LatLonMixin):
    date_created = Column(Date)


@implementer(IVillage)
class Village(Base, IdNameDescriptionMixin, HasFilesMixin, LatLonMixin):
    languoid_pk = Column(Integer, ForeignKey('languoid.pk'))
    languoid = relationship(Languoid, backref='villages')
    surnames = Column(Unicode)
    major_city = Column(Boolean)
    transcribed_name = Column(Unicode)
    source_of_coordinates = Column(Unicode)


@implementer(IFile)
class File(Base, IdNameDescriptionMixin):
    # id: md5 checksum
    # name: filename
    size = Column(Integer)
    date_created = Column(Date)
    mime_type = Column(Unicode)


class Fotographer(Base):
    foto_pk = Column(Integer, ForeignKey('village_files.pk'))
    contributor_pk = Column(Integer, ForeignKey('contributor.pk'))

    foto = relationship(Village_files, backref='contributor_assocs')
    contributor = relationship(Contributor, lazy=False, backref='foto_assocs')
