from clld.web.maps import ParameterMap, Map


def _opts():
    return {
        'show_labels': True,
        'max_zoom': 12,
        'base_layer': "MapQuestOpen.Aerial",
    }


class LanguagesMap(Map):
    def get_options(self):
        opts = Map.get_options(self)
        opts.update(_opts())
        return opts


class ConceptMap(ParameterMap):
    def get_options(self):
        opts = ParameterMap.get_options(self)
        opts.update(_opts())
        return opts


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('parameter', ConceptMap)
