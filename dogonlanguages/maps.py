from clld.web.maps import ParameterMap, Map
from clld.util import dict_merged


OPTIONS = {'show_labels': True, 'max_zoom': 12, 'base_layer': "MapQuestOpen.Aerial"}


class LanguagesMap(Map):
    def get_options(self):
        return dict_merged(Map.get_options(self), **OPTIONS)


class ConceptMap(ParameterMap):
    def get_options(self):
        return dict_merged(ParameterMap.get_options(self), **OPTIONS)


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('parameter', ConceptMap)
