from sqlalchemy.orm import joinedload

from clld.interfaces import IParameter, ILanguage
from clld.web.adapters import GeoJsonParameter, GeoJson
from clld.db.meta import DBSession
from clld import interfaces

from dogonlanguages.interfaces import IVillage
from dogonlanguages.models import Village


class GeoJsonConcept(GeoJsonParameter):
    def feature_properties(self, ctx, req, valueset):
        return {
            'values': list(valueset.values),
            'label': ', '.join(v.name for v in valueset.values)}


class GeoJsonLanguage(GeoJson):
    def feature_iterator(self, ctx, req):
        return DBSession.query(Village)\
            .filter(Village.languoid == ctx)\
            .options(joinedload(Village.languoid))


class GeoJsonVillages(GeoJson):
    def feature_iterator(self, ctx, req):
        return DBSession.query(Village).options(joinedload(Village.languoid))


def includeme(config):
    config.register_adapter(GeoJsonConcept, IParameter)
    config.register_adapter(GeoJsonLanguage, ILanguage)
    config.register_adapter(
        GeoJsonVillages, IVillage, interfaces.IIndex, name=GeoJson.mimetype)
