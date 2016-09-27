from functools import partial

from pyramid.config import Configurator

from clld.web.app import menu_item

# we must make sure custom models are known at database initialization!
from dogonlanguages import models
from dogonlanguages.interfaces import IVillage
from dogonlanguages import views


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['route_patterns'] = {
        'villages': '/geography.cfm',
        'parameters': '/thesaurus.cfm',
        'sources': '/bibliography.cfm',
        'languages': '/languages.cfm',
        'florafauna': '/florafauna.cfm',
        'bangime': '/bangime.cfm',
    }
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('languages', partial(menu_item, 'languages')),
        ('values', partial(menu_item, 'values', label='Lexicon')),
        ('parameters', partial(menu_item, 'parameters', label='Thesaurus')),
        ('villages', partial(menu_item, 'villages', label='Villages')),
        ('florafauna', partial(menu_item, 'florafauna', label='Flora-Fauna')),
        ('contributors', partial(menu_item, 'contributors', label='Project members')),
        ('sources', partial(menu_item, 'sources', label='Bibliography')),
        ('bangime', partial(menu_item, 'bangime', label='Bangime')),
        ('other', partial(menu_item, 'other', label='Other Languages')),
    )
    config.register_resource('village', models.Village, IVillage, with_index=True)
    # must register snippet adapter for villages!

    config.add_page('bangime')
    config.add_page('florafauna')
    config.add_page('other')

    return config.make_wsgi_app()
