from __future__ import unicode_literals
from textwrap import wrap

from sqlalchemy.orm import joinedload_all, joinedload

from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.contributor import Contributors, NameCol, UrlCol
from clld.web.datatables.source import Sources, TypeCol
from clld.web.datatables.language import Languages
from clld.web.datatables.base import LinkCol, Col, DataTable, LinkToMapCol, DetailsRowLinkCol
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import icon, link
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import get_distinct_values

from dogonlanguages import models
from dogonlanguages import util


class DogonLanguages(Languages):
    def base_query(self, query):
        return Languages.base_query(self, query).filter(models.Languoid.in_project == True)


class ProjectMembers(Contributors):
    def col_defs(self):
        return [
            NameCol(self, 'name'),
            Col(self, 'description'),
            UrlCol(self, 'Homepage'),
        ]


class VideosCol(Col):
    __kw__ = {'input_size': 'mini'}

    def format(self, item):
        item = self.get_obj(item)
        if item.count_videos:
            return HTML.span(
                '%s' % item.count_videos, icon('film', inverted=True), class_='badge')
        return ''


class ImagesCol(Col):
    __kw__ = {'input_size': 'mini'}

    def format(self, item):
        item = self.get_obj(item)
        if item.count_images:
            return HTML.span(
                '%s' % item.count_images, icon('camera', inverted=True), class_='badge')
        return ''


class TsammalexCol(Col):
    def format(self, item):
        return util.tsammalex_link(self.dt.req, item)


class ConcepticonCol(Col):
    def format(self, item):
        return util.concepticon_link(self.dt.req, item)


class Concepts(Parameters):
    def base_query(self, query):
        return query.join(models.Subdomain).join(models.Domain)

    def col_defs(self):
        return [
            Col(self, 'ID', model_col=common.Parameter.id),
            LinkCol(self, 'gloss', model_col=common.Parameter.name),
            Col(self, 'domain',
                choices=get_distinct_values(models.Domain.name),
                get_object=lambda i: i.subdomain.domain,
                model_col=models.Domain.name),
            Col(self, 'subdomain',
                choices=get_distinct_values(models.Subdomain.name),
                get_object=lambda i: i.subdomain,
                model_col=models.Subdomain.name),
            ConcepticonCol(
                self, 'concepticon',
                input_size='mini',
                model_col=models.Concept.concepticon_id),
            TsammalexCol(
                self, 'tsammalex',
                input_size='mini',
                model_col=models.Concept.tsammalex_taxon),
            ImagesCol(self, 'images', model_col=models.Concept.count_images),
            VideosCol(self, 'videos', model_col=models.Concept.count_videos),
        ]


class Words(Values):
    def __init__(self, req, model, **kw):
        Values.__init__(self, req, model, **kw)
        self.ff = False
        if kw.get('ff') or 'ff' in req.params:
            self.ff = True

    def xhr_query(self):
        res = Values.xhr_query(self)
        if self.ff:
            res['ff'] = 1
        return res

    def base_query(self, query):
        query = query.join(common.ValueSet)

        if self.language:
            query = query.join(common.ValueSet.parameter)
            return query.filter(common.ValueSet.language_pk == self.language.pk)

        if self.parameter:
            query = query.join(common.ValueSet.language)
            return query.filter(common.ValueSet.parameter_pk == self.parameter.pk)

        query = query\
            .join(common.Parameter)\
            .join(common.Language)\
            .join(models.Subdomain)\
            .join(models.Domain)\
            .options(
                joinedload_all(
                    common.Value.valueset,
                    common.ValueSet.parameter,
                    models.Concept.subdomain,
                    models.Subdomain.domain),
                joinedload(common.Value.valueset, common.ValueSet.language)
            )
        if self.ff:
            query = query.filter(models.Domain.name.in_(['flora', 'fauna']))
        return query

    def col_defs(self):
        if self.language:
            return [
                LinkCol(
                    self, 'concept',
                    get_object=lambda item: item.valueset.parameter,
                    model_col=common.Parameter.name),
                Col(self, 'domain',
                    get_object=lambda item: item.valueset.parameter.subdomain.domain,
                    model_col=models.Domain.name),
                Col(self, 'subdomain',
                    get_object=lambda item: item.valueset.parameter.subdomain,
                    model_col=models.Subdomain.name),
                LinkCol(self, 'word', model_col=common.Value.name),
                ]
        if self.parameter:
            return [
                LinkCol(
                    self, 'language',
                    get_object=lambda item: item.valueset.language,
                    model_col=common.Language.name),
                LinkCol(self, 'word', model_col=common.Value.name),
            ]
        res = [
            LinkCol(
                self, 'language',
                get_object=lambda item: item.valueset.language,
                model_col=common.Language.name),
            LinkCol(
                self, 'concept',
                get_object=lambda item: item.valueset.parameter,
                model_col=common.Parameter.name),
            ImagesCol(
                self, '#',
                get_object=lambda i: i.valueset.parameter,
                model_col=models.Concept.count_images),
            Col(self, 'domain',
                get_object=lambda item: item.valueset.parameter.subdomain.domain,
                model_col=models.Domain.name),
            Col(self, 'subdomain',
                get_object=lambda item: item.valueset.parameter.subdomain,
                model_col=models.Subdomain.name),
            LinkCol(self, 'word', model_col=common.Value.name),
            Col(self, 'literal meaning', model_col=common.Value.description),
            Col(self, 'note', model_col=models.Counterpart.comment),
        ]
        return res


class LanguoidCol(Col):
    def __init__(self, dt, name, **kw):
        sq = DBSession.query(models.Village.languoid_pk).distinct().subquery()
        kw['choices'] = [
            (l.id, l.name) for l in
            DBSession.query(common.Language).filter(common.Language.pk.in_(sq))]
        Col.__init__(self, dt, name, **kw)

    def search(self, qs):
        return common.Language.id == qs

    def order(self):
        return common.Language.name

    def format(self, item):
        if item.languoid:
            if item.languoid.in_project:
                return link(self.dt.req, item.languoid)
            return item.languoid.name


class ImageCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        if item._files:
            return HTML.span('%s' % len(item._files), icon('camera', inverted=True), class_='badge')
        return ''


class Villages(DataTable):
    def base_query(self, query):
        return query\
            .outerjoin(models.Village.languoid)\
            .outerjoin(models.Village._files)\
            .options(
                joinedload(models.Village.languoid),
                joinedload(models.Village._files),
            )

    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            LinkToMapCol(self, '_'),
            ImageCol(self, '#'),
            LanguoidCol(self, 'language (group)'),
            Col(self, 'major city', model_col=models.Village.major_city),
            Col(self, 'surnames', model_col=models.Village.surnames),
        ]


class DocumentCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        if item._files:
            return HTML.span('%s' % len(item._files), icon('file', inverted=True), class_='badge')
        return ''


class Documents(Sources):
    def col_defs(self):
        return [
            DetailsRowLinkCol(self, 'd'),
            LinkCol(self, 'name'),
            Col(self, 'description', sTitle='Title'),
            Col(self, 'year', input_size='mini'),
            Col(self, 'author'),
            Col(self, 'DLP', sTitle='DLP', model_col=models.Document.project_doc),
            Col(self, 'type',
                input_size='mini',
                model_col=models.Document.doctype,
                choices=get_distinct_values(models.Document.doctype)),
            DocumentCol(self, '#'),
            TypeCol(self, 'bibtex_type'),
        ]


class ViewCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return HTML.a(
            icon('eye-open'),
            href=util.cdstar_url(item),
            title='view',
            class_="btn")


def wrap_fname(i):
    return '_ ... _'.join(
        s.replace(' ', '_') for s in wrap(i.name.replace('_', ' '), width=60))


class Files(DataTable):
    def col_defs(self):
        return [
            Col(self, 'name', format=wrap_fname),
            ViewCol(self, 'view'),
            Col(self, 'size', format=lambda i: util.format_size(i)),
            Col(self, 'mime_type', sTitle='media type', choices=get_distinct_values(models.File.mime_type)),
            Col(self, 'date', model_col=models.File.date_created, bSearchable=False),
            # TODO: link to download!
            Col(self, 'id', sTitle='MD5 checksum'),
        ]


def includeme(config):
    config.register_datatable('contributors', ProjectMembers)
    config.register_datatable('languages', DogonLanguages)
    config.register_datatable('parameters', Concepts)
    config.register_datatable('values', Words)
    config.register_datatable('villages', Villages)
    config.register_datatable('files', Files)
    config.register_datatable('sources', Documents)
