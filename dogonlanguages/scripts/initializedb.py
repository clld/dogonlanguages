from __future__ import unicode_literals
import sys
import re

from sqlalchemy import create_engine

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.dsv import reader
from clld.util import slug, nfilter

import dogonlanguages
from dogonlanguages import models
from dogonlanguages.scripts import util


f = [
"code_eng",  # category
"subcode_eng",  # subcategory
"code_fr",
"sous_code_fr",
"code", "subcode", "subsubcode",  # make up id!
"short",
"court",
"ref",
"jpg",
"video",
"date",
"comment",
"English",  # meaning
"Francais",
"core",  # 1 or 0
]

LANGUAGES = [
    ("Toro_Tegu", 'toro1253'),
    ("Ben_Tey", 'bent1238'),
    ("Bankan_Tey", 'bank1259'),
    ("Nanga", 'nang1261'),
    ("Jamsay_Alphabet", 'jams1239'),
    ("Jamsay", 'jams1239'),
    ("Perge_Tegu", ''),
    ("Gourou", ''),
    ("Jamsay_Mondoro", ''),
    ("Togo_Kan", ''),
    ("Yorno_So", ''),
    ("Tomo_Kan", 'tomo1243'),
    ("Tomo_Kan_Diangassagou", ''),
    ("Tommo_So", ''),
    ("Dogul_Dom", 'dogu1235'),
    ("Tebul_Ure", 'tebu1239'),
    ("Yanda_Dom", 'yand1257'),
    ("Najamba", ''),
    ("Tiranige", 'tira1258'),
    ("Mombo", 'momb1254'),
    ("Ampari", 'ampa1238'),
    ("Bunoge", 'buno1241'),
    ("Penange", 'pena1270'),
]


def main(args):
    gl = create_engine('postgresql://robert@/glottolog3')
    data = Data()

    dataset = common.Dataset(
        id=dogonlanguages.__name__,
        name="Dogon and Bangime Linguistics",
        publisher_name ="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/3.0/",
        domain='dogonlanguages.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 3.0 Unported License'}
    )
    DBSession.add(dataset)

    for name, props in util.CONTRIBUTORS.items():
        id_ = slug(name.split()[-1])
        data.add(
            common.Contributor, id_,
            id=id_, name=name, description=props[0], email=props[1], url=props[2])

    for i, spec in enumerate([
            ('heath', "Jeffrey Heath"),
    ]):
        DBSession.add(common.Editor(
            dataset=dataset,
            ord=i + 1,
            contributor=data['Contributor'][spec[0]]))

    contrib = data.add(common.Contribution, 'd', id='d', name='Dogon Languages')

    names = {}
    for concept in reader(args.data_file('dogon_lexicon.csv'), delimiter=',', namedtuples=True):
        code = data['Code'].get(concept.code)
        if code is None:
            code = data.add(
                models.Code, concept.code,
                id=concept.code,
                name=concept.code_eng,
                description=concept.code_fr)
        scid = '-'.join([concept.code, concept.subcode.replace('.', '_')])
        subcode = data['SubCode'].get(scid)
        if subcode is None:
            try:
                subcode = data.add(
                    models.SubCode, scid,
                    id=scid,
                    name=concept.subcode_eng,
                    description=concept.sous_code_fr,
                    code=code)
            except:
                print scid, concept.English
                continue
        cid = '-'.join([scid, concept.subsubcode.replace('.', '_')])
        if cid in data['Concept']:
            print '-->', cid, concept.English
            print data['Concept'][cid].name
            continue

        if concept.English in names:
            name = '%s (2)' % concept.English
        else:
            name = concept.English
            names[name] = 1

        try:
            c = data.add(
                models.Concept, cid,
                core=concept.core == '1',
                id=cid,
                name=name,
                description=concept.Francais,
                subcode=subcode)
        except:
            print cid, concept.English
            continue

        for l, gc in LANGUAGES:
            if gc:
                lat, lon = gl.execute(
                    'select latitude, longitude from language where id = %s', (gc,))\
                    .fetchone()
            else:
                lat, lon = None, None
            lid = slug(l)
            lang = data['Language'].get(lid)
            if lang is None:
                lang = data.add(
                    common.Language, lid,
                    id=lid, name=l.replace('_', ' '), latitude=lat, longitude=lon)

            forms = (getattr(concept, l) or '').strip()
            if not forms:
                continue

            vs = common.ValueSet(
                id='-'.join([lid, cid]),
                language=lang,
                contribution=contrib,
                parameter=c)
            for i, form in enumerate(nfilter(re.split('\s*,\s*', forms))):
                v = common.Value(id='-'.join([cid, lid, str(i + 1)]), valueset=vs, name=form)

        #
        # TODO: identify forms!
        #


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
