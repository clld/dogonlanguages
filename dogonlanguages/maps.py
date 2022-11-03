from collections import defaultdict

from clld.interfaces import IMapMarker
from clld.web.maps import ParameterMap, Map, Legend, Layer
from clld.web.adapters.geojson import GeoJson, get_lonlat
from clld.web.util.htmllib import HTML
from clld.web.icon import MapMarker as BaseMapMarker
from clldutils.misc import dict_merged

from dogonlanguages.interfaces import IVillage
from dogonlanguages.scripts.data import LANGUAGES


OPTIONS = {'show_labels': True, 'max_zoom': 12, 'base_layer': "Esri.WorldImagery"}


class VillageGeoJson(GeoJson):
    def feature_iterator(self, ctx, req):
        return [ctx]


class VillageMap(Map):

    def get_layers(self):
        yield Layer(
            self.ctx.id,
            self.ctx.name,
            VillageGeoJson(self.ctx).render(self.ctx, self.req, dump=False))

    def get_default_options(self):
        return {
            'center': list(reversed(get_lonlat(self.ctx) or [0, 0])),
            'max_zoom': 15,
            'no_popup': True,
            'no_link': True,
            'sidebar': True}


class LanguagesMap(Map):
    def get_options(self):
        return dict_merged(Map.get_options(self), **OPTIONS)


class DogonLanguageMap(Map):
    def get_options(self):
        res = dict_merged(Map.get_options(self), **OPTIONS)
        res.update({
            #'center': list(reversed(get_lonlat(self.ctx) or [0, 0])),
            #'zoom': 3,
            'max_zoom': 15,
            'no_popup': True,
            'no_link': True,
            'sidebar': True})
        return res


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

GC_TO_NAME = {v[0]: k for k, v in LANGUAGES.items()}


class MapMarker(BaseMapMarker):
    def get_icon(self, ctx, req):
        if IVillage.providedBy(ctx):
            if ctx.languoid and ctx.languoid.family == 'Dogon':
                return DOGON_MARKER[ctx.languoid.id]
            return FAMILY_MARKER[getattr(ctx.languoid, 'family', 'unknown')]
        return BaseMapMarker.get_icon(self, ctx, req)  # pragma: no cover


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

        def header(label):
            return HTML.h5(label, style='padding-left:5px;margin-top:0;margin-bottom:0')

        def make_item(label, icon):
            return HTML.span(
                HTML.img(
                    width=16,
                    height=16,
                    src=self.req.static_url('clld:web/static/icons/%s.png' % icon)),
                HTML.span(label, style='padding-left:5px'),
                style='padding-left:5px')

        items = [header('Dogon')]
        items.extend(
            [make_item(GC_TO_NAME[gc], icon) for gc, icon in DOGON_MARKER.items()])
        items.append(header('Other'))
        items.extend(
            [make_item(name, icon) for name, icon in FAMILY_MARKER.items() if name != 'Dogon'])
        items.append(make_item('unknown', FAMILY_MARKER['x']))
        yield Legend(self, 'families', items)


def includeme(config):
    config.registry.registerUtility(MapMarker(), IMapMarker)
    config.register_map('language', DogonLanguageMap)
    config.register_map('languages', LanguagesMap)
    config.register_map('parameter', ConceptMap)
    config.register_map('village', VillageMap)
    config.register_map('villages', VillagesMap)
