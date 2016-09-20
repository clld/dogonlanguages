from collections import defaultdict

from clld.interfaces import IMapMarker
from clld.web.maps import ParameterMap, Map, Legend
from clld.web.util.htmllib import HTML
from clld.web.icon import MapMarker as BaseMapMarker
from clldutils.misc import dict_merged

from dogonlanguages.interfaces import IVillage


OPTIONS = {'show_labels': True, 'max_zoom': 12, 'base_layer': "Esri.WorldImagery"}


class LanguagesMap(Map):
    def get_options(self):
        return dict_merged(Map.get_options(self), **OPTIONS)


class ConceptMap(ParameterMap):
    def get_options(self):
        return dict_merged(ParameterMap.get_options(self), **OPTIONS)


#
# FIXME: distinguish: other families: circle, dogon: triangle, unknown: upside down triangle.
# for dogon distinguish languages by color!
#
FAMILY_MARKER = defaultdict(lambda: 'fff6600', **{
    'Songhay': 'c0000dd',
    'Atlantic-Congo': 'c009900',
    'Bangime': 'caa0000',
    'Afro-Asiatic': 'c000000',
    'Mande': 'ce8e8e8',
    'Dogon': 'cffff00',
})

DOGON_MARKER = {
    "bent1238": "t0000ff",
    "bank1259": "t99ffff",
    "nang1261": "te8e8e8",
    "togo1254": "tcccccc",
    "tomm1242": "t0000dd",
    "donn1238": "t4d6cee",
    "yorn1234": "t9999ff",

    "jams1239": "t00ffff",
    "tomo1243": "t66ff33",
    "toro1252": "t009900",
    "toro1253": "ta0fb75",

    "perg1234": "taa0000",
    "guru1265": "td22257",
    "dogu1235": "tdd0000",
    "tebu1239": "tfe3856",
    "yand1257": "tff0000",
    "bond1248": "tff66ff",

    "tira1258": "ted9c07",
    "momb1254": "tf3ffb0",
    "ampa1238": "tff6600",
    "buno1241": "tefe305",
    "pena1270": "tffcc00",
}


class MapMarker(BaseMapMarker):
    def get_icon(self, ctx, req):
        if IVillage.providedBy(ctx):
            if ctx.languoid and ctx.languoid.family == 'Dogon':
                return DOGON_MARKER[ctx.languoid.id]
            return FAMILY_MARKER[getattr(ctx.languoid, 'family', 'unknown')]
        return BaseMapMarker.get_icon(self, ctx, req)


class VillagesMap(Map):
    def get_options(self):
        res = dict_merged(Map.get_options(self), **OPTIONS)
        del res['show_labels']
        res['info_route'] = 'village_alt'
        res['icon_size'] = 15
        return res

    def get_legends(self):
        for legend in Map.get_legends(self):
            yield legend
        items = [
            HTML.span(HTML.img(src=self.req.static_url('clld:web/static/icons/%s.png' % u)), HTML.span(l))
            for l, u in list(FAMILY_MARKER.items()) + [('unknown', FAMILY_MARKER['x'])]]
        yield Legend(self, 'families', items)


def includeme(config):
    config.registry.registerUtility(MapMarker(), IMapMarker)
    config.register_map('languages', LanguagesMap)
    config.register_map('parameter', ConceptMap)
    config.register_map('villages', VillagesMap)
