from clld.web.assets import environment
from clldutils.path import Path

import dogonlanguages


environment.append_path(
    Path(dogonlanguages.__file__).parent.joinpath('static').as_posix(),
    url='/dogonlanguages:static/')
environment.load_path = list(reversed(environment.load_path))
