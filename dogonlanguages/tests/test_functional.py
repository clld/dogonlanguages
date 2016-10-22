from clldutils.path import Path

from clld.tests.util import TestWithApp

import dogonlanguages


class Tests(TestWithApp):
    __cfg__ = Path(dogonlanguages.__file__).parent.joinpath('..', 'development.ini')

    def test_home(self):
        self.app.get('/')
        self.app.get_dt('/contributors')
        self.app.get_dt('/thesaurus.cfm')
        self.app.get_dt('/values')
        self.app.get_dt('/languages.cfm')
        self.app.get_dt('/bibliography.cfm')
        self.app.get_dt('/geography.cfm')
        self.app.get('/contributors')
        self.app.get('/thesaurus.cfm')
        self.app.get('/values')
        self.app.get('/languages.cfm')
        self.app.get('/bibliography.cfm')
        self.app.get('/geography.cfm')
        self.app.get('/villages/638')
        self.app.get_json('/geography.cfm.geojson')
        self.app.get('/villages/1002')
        self.app.get('/typology')

    def test_parameter(self):
        self.app.get_html('/parameters/60591')
        self.app.get_html('/parameters/50283')
        self.app.get_html('/parameters/01767')
        self.app.get_json('/parameters/01767.geojson')

    def test_pages(self):
        self.app.get('/other')
        self.app.get('/florafauna.cfm')
        self.app.get('/bangime.cfm')

    def test_movies(self):
        self.app.get('/movies')
        self.app.get_dt('/movies')

    def test_language(self):
        self.app.get('/languages/ampa1238')
        self.app.get_json('/languages/ampa1238.geojson')

    def test_values(self):
        self.app.get_dt('/values?parameter=00001')
        self.app.get_dt('/values?language=ampa1238')
