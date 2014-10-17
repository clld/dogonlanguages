from __future__ import unicode_literals
import sys
import re
from collections import defaultdict

from sqlalchemy import create_engine

from clld.scripts.util import initializedb, Data, bibtex2source
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
    # fauna has also:
    #Ibi-So (JH),
    #Donno-So,
    ("Tomo_Kan", 'tomo1243'),
    ("Tomo_Kan_Diangassagou", ''),
    ("Tommo_So", ''),
    #"Tommo So (Tongo Tongo, JH)",
    #"Tommo-So (Tongo Tongo, LM)",
    ("Dogul_Dom", 'dogu1235'),
    ("Tebul_Ure", 'tebu1239'),
    ("Yanda_Dom", 'yand1257'),
    ("Najamba", ''),
    ("Tiranige", 'tira1258'),
    ("Mombo", 'momb1254'),
    ("Ampari", 'ampa1238'),
    ("Bunoge", 'buno1241'),
    ("Penange", 'pena1270'),
    #"Bangime (Bounou, JH)",
    #"Bangime (Bounou, AH)",
    # HS Songhay,
    # TSK Songhay,
]


def main(args):
    files_dir = args.data_file('files')
    files_dir.mkdir_p()
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

    for rec in util.get_bib(args):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    names = defaultdict(int)
    cids = {}
    for concept in reader(args.data_file('fauna_Dogon_Unicode.csv'), delimiter=',', dicts=True):
        add(cids, gl, util.ff_to_standard(concept), data, names, contrib, ff=True)

    for concept in reader(args.data_file('dogon_lexicon.csv'), delimiter=',', namedtuples=True):
        add(cids, gl, concept, data, names, contrib)

    ref_pattern = re.compile('(?P<ref>[0-9]{5})')
    count = 0
    for i, img in enumerate(reader(args.data_file('dogon_flora-fauna.csv'), delimiter=',', namedtuples=True)):
        match = ref_pattern.search(img.filenames)
        if match and match.group('ref') in data['Concept']:
            #print 'image for', data['Concept'][match.group('ref')].name
            concept = data['Concept'][match.group('ref')]
            content = util.get_thumbnail(args, img.filenames)
            if content:
                ext = img.filenames.lower().split('.')[-1]
                f = common.Parameter_files(
                    object=concept,
                    id=str(i + 1) + '.' + ext,
                    name=img.filenames,
                    mime_type='image/tiff' if ext.startswith('tif') else 'image/jpeg')
                f.create(files_dir, content)
                count += 1
    print count, 'images detected'


def add(cids, gl, concept, data, names, contrib, ff=False):
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
            return
    cid = '-'.join([scid, concept.subsubcode.replace('.', '_')])
    if cid in data['Concept']:
        print '-->', cid, concept.English
        print data['Concept'][cid].name
        return

    if concept.English in names:
        name = '%s (%s)' % (concept.English, names[concept.English] + 1)
    else:
        name = concept.English
    names[concept.English] += 1

    if cid in cids:
        print '***', cid, concept.ref, concept.English
        return
    cids[cid] = 1

    c = data['Concept'].get(concept.ref)
    if c is None:
        c = data.add(
            models.Concept, concept.ref,
            core=concept.core == '1',
            id=cid,
            name=name,
            ref=int(concept.ref),
            ff=ff,
            description=concept.Francais,
            subcode=subcode)
        if ff:
            c.species = concept.species
            c.family = concept.family
    else:
        print '***', cid, concept.ref, concept.English
        return

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
