from path import path

from clld.tests.util import TestWithApp

import dogonlanguages


class Tests(TestWithApp):
    __cfg__ = path(dogonlanguages.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get('/')
        self.app.get_dt('/contributors')
        self.app.get_dt('/parameters')
        self.app.get_dt('/values')
        self.app.get_dt('/languages')
        self.app.get('/contributors')
        self.app.get('/parameters')
        self.app.get('/values')
        self.app.get('/languages')
