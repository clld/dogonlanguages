from zope.interface import implementer
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
class Concept(Parameter, CustomModelMixin):
    """one row in what used to be the word-meaning association table
    """
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)

    core = Column(Boolean, nullable=False)
    subcode_pk = Column(Integer, ForeignKey('subcode.pk'))
    subcode = relationship(SubCode, backref='concepts')


@implementer(interfaces.IValue)
class Counterpart(Value, CustomModelMixin):
    """one row in what used to be the word-meaning association table
    """
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)

    unit_pk = Column(Integer, ForeignKey('unit.pk'))
    unit = relationship(Unit, backref='counterparts')
