import pathlib

from clld.web.assets import environment

import dogonlanguages


environment.append_path(
    str(pathlib.Path(dogonlanguages.__file__).parent.joinpath('static')),
    url='/dogonlanguages:static/')
environment.load_path = list(reversed(environment.load_path))
