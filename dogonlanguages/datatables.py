from sqlalchemy.orm import joinedload_all, joinedload

from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.contributor import Contributors, NameCol, UrlCol
from clld.web.datatables.language import Languages
from clld.web.datatables.base import LinkCol, Col, DataTable, LinkToMapCol
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import icon, link
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import get_distinct_values

from dogonlanguages import models


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


class ThumbnailCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        item = self.get_obj(item)
        if item.thumbnail:
            return HTML.img(class_='img-rounded', src=self.dt.req.file_url(item.thumbnail))
        if item.video:
            return icon('film')
        return ''


class Concepts(Parameters):
    def base_query(self, query):
        return query.join(models.Subdomain).join(models.Domain)

    def col_defs(self):
        return [
            Col(self, 'ID', model_col=common.Parameter.id),
            LinkCol(self, 'gloss', model_col=common.Parameter.name),
            ThumbnailCol(self, 'thumbnail'),
            Col(self, 'domain',
                choices=get_distinct_values(models.Domain.name),
                get_object=lambda i: i.subdomain.domain,
                model_col=models.Domain.name),
            Col(self, 'subdomain',
                choices=get_distinct_values(models.Subdomain.name),
                get_object=lambda i: i.subdomain,
                model_col=models.Subdomain.name)
        ]


class Words(Values):
    def base_query(self, query):
        query = query.join(common.ValueSet)

        if self.language:
            query = query.join(common.ValueSet.parameter)
            return query.filter(common.ValueSet.language_pk == self.language.pk)

        if self.parameter:
            query = query.join(common.ValueSet.language)
            return query.filter(common.ValueSet.parameter_pk == self.parameter.pk)

        return query\
            .join(common.Parameter)\
            .join(models.Subdomain)\
            .join(models.Domain)\
            .options(
                joinedload_all(
                    common.Value.valueset,
                    common.ValueSet.parameter,
                    models.Concept.subdomain,
                    models.Subdomain.domain)
            )

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
                bSortable=False, bSearchable=False),
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


def includeme(config):
    config.register_datatable('contributors', ProjectMembers)
    config.register_datatable('languages', DogonLanguages)
    config.register_datatable('parameters', Concepts)
    config.register_datatable('values', Words)
    config.register_datatable('villages', Villages)
