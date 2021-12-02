from functools import partial

from pyramid.config import Configurator
from sqlalchemy.orm import joinedload

from clld.web.app import menu_item, CtxFactoryQuery
from clld.db.models import common
from clld.interfaces import ICtxFactoryQuery

# we must make sure custom models are known at database initialization!
from dogonlanguages import models
from dogonlanguages.interfaces import IVillage, IFile, IMovie
from dogonlanguages import views


_ = lambda s: s
_('Parameters')
_('Sources')
_('Contributors')
_('Other')


class CustomFactoryQuery(CtxFactoryQuery):
    def refined_query(self, query, model, req):
        """To be overridden.

        Derived classes may override this method to add model-specific query
        refinements of their own.
        """
        if model == common.Contribution:
            query = query.options(
                joinedload(common.Contribution.references)
                .joinedload(common.ContributionReference.source),
                joinedload(common.Contribution.data),
            )
        return query


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
        'file': r'/_files/{id:[^/\.]+}',
        'file_alt': r'/_files/{id:[^/\.]+}.{ext}',
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
        #('contributors', partial(menu_item, 'contributors', label='Project members')),
        ('sources', partial(menu_item, 'sources', label='Materials')),
        #('bangime', partial(menu_item, 'bangime', label='Bangime')),
        #('other', partial(menu_item, 'other', label='Other Languages')),
        ('movies', partial(menu_item, 'movies', label='Videos')),
    )
    home_comp = config.registry.settings['home_comp']
    home_comp = [
        'bangime', 'other',
        'contributors'] + home_comp
    config.add_settings({'home_comp': home_comp})
    config.register_resource('village', models.Village, IVillage, with_index=True)
    config.register_resource('movie', models.Movie, IMovie, with_index=True)
    config.register_resource('file', models.File, IFile, with_index=True)
    config.registry.registerUtility(CustomFactoryQuery(), ICtxFactoryQuery)
    config.add_page('bangime')
    config.add_page('florafauna')
    config.add_page('other')
    config.add_page('typology')

    return config.make_wsgi_app()
