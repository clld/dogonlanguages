from zope.interface import implementer
from pyramid.decorator import reify
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import IdNameDescriptionMixin, Value, Unit, Parameter


class Code(Base, IdNameDescriptionMixin):
    pass


class SubCode(Base, IdNameDescriptionMixin):
    code_pk = Column(Integer, ForeignKey('code.pk'))
    code = relationship(Code, backref='subcodes')


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
    subcode_pk = Column(Integer, ForeignKey('subcode.pk'))
    subcode = relationship(SubCode, backref='concepts')

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


@implementer(interfaces.IValue)
class Counterpart(CustomModelMixin, Value):
    """one row in what used to be the word-meaning association table
    """
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)

    comment = Column(Unicode)
    unit_pk = Column(Integer, ForeignKey('unit.pk'))
    unit = relationship(Unit, backref='counterparts')
