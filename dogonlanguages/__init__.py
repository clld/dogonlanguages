from functools import partial

from clld.web.app import get_configurator, menu_item

# we must make sure custom models are known at database initialization!
from dogonlanguages import models


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = get_configurator('dogonlanguages', settings=settings)
    config.include('clldmpg')
    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('languages', partial(menu_item, 'languages')),
        ('values', partial(menu_item, 'values', label='Lexicon')),
        ('parameters', partial(menu_item, 'parameters', label='Thesaurus')),
        ('contributors', partial(menu_item, 'contributors', label='Project members')),
        ('sources', partial(menu_item, 'sources', label='Bibliography')),
    )
    return config.make_wsgi_app()
