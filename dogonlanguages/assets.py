from clld.web.assets import environment
from path import path

import dogonlanguages


environment.append_path(
    path(dogonlanguages.__file__).dirname().joinpath('static'), url='/dogonlanguages:static/')
environment.load_path = list(reversed(environment.load_path))
