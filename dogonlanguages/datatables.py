from sqlalchemy.orm import joinedload_all

from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.contributor import Contributors, NameCol, UrlCol
from clld.web.datatables.base import LinkCol, Col, IdCol
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import get_distinct_values

from dogonlanguages import models


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
        return ''


class Concepts(Parameters):
    def base_query(self, query):
        return query.join(models.SubCode).join(models.Code)

    def col_defs(self):
        return [
            Col(self, 'ID', model_col=common.Parameter.id),
            LinkCol(self, 'gloss', model_col=common.Parameter.name),
            ThumbnailCol(self, 'thumbnail'),
            Col(self, 'domain',
                choices=get_distinct_values(models.Code.name),
                get_object=lambda i: i.subcode.code,
                model_col=models.Code.name),
            Col(self, 'subdomain',
                choices=get_distinct_values(models.SubCode.name),
                get_object=lambda i: i.subcode,
                model_col=models.SubCode.name)
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
            .join(models.SubCode)\
            .join(models.Code)\
            .options(
                joinedload_all(
                    common.Value.valueset,
                    common.ValueSet.parameter,
                    models.Concept.subcode,
                    models.SubCode.code)
            )

    def col_defs(self):
        if self.language:
            return [
                LinkCol(
                    self, 'concept',
                    get_object=lambda item: item.valueset.parameter,
                    model_col=common.Parameter.name),
                Col(self, 'code',
                    get_object=lambda item: item.valueset.parameter.subcode.code,
                    model_col=models.Code.name),
                Col(self, 'subcode',
                    get_object=lambda item: item.valueset.parameter.subcode,
                    model_col=models.SubCode.name),
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
                get_object=lambda item: item.valueset.parameter.subcode.code,
                model_col=models.Code.name),
            Col(self, 'subdomain',
                get_object=lambda item: item.valueset.parameter.subcode,
                model_col=models.SubCode.name),
            LinkCol(self, 'word', model_col=common.Value.name),
        ]
        return res


def includeme(config):
    config.register_datatable('contributors', ProjectMembers)
    config.register_datatable('parameters', Concepts)
    config.register_datatable('values', Words)
