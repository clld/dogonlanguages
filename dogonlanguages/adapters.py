from __future__ import unicode_literals, division, absolute_import, print_function

from clld.interfaces import IParameter
from clld.web.adapters import GeoJsonParameter


class GeoJsonConcept(GeoJsonParameter):
    def feature_properties(self, ctx, req, valueset):
        return {
            'values': list(valueset.values),
            'label': ', '.join(v.name for v in valueset.values)}


def includeme(config):
    config.register_adapter(GeoJsonConcept, IParameter)
