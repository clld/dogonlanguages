from __future__ import unicode_literals
import sys
import re
from collections import defaultdict, Counter
from mimetypes import guess_type

import attr
from purl import URL
from clldutils.dsv import reader
from clldutils.misc import slug, nfilter
from clldutils import jsonlib
from clldutils.path import Path

from clld.scripts.util import initializedb, Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
try:
    from pyglottolog.api import Glottolog
except ImportError:
    Glottolog = None

import dogonlanguages
from dogonlanguages import models
from dogonlanguages.scripts import util
from dogonlanguages.scripts.data import LANGUAGES, LEX_LANGS


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


def main(args):
    village_images = {f.path.stem: f for f in util.village_images(args)}
    print('got %s images' % len(village_images))

    if Glottolog:
        glottolog = Glottolog(
            Path(dogonlanguages.__file__).parent.parent.parent.parent.joinpath(
                'glottolog3', 'glottolog'))
        languoids = {l.id: l for l in glottolog.languoids()}
    else:
        languoids = {}
    print('got glottolog')

    files_dir = args.data_file('files')
    if not files_dir.exists():
        files_dir.mkdir(parents=True)
    data = Data()

    dataset = common.Dataset(
        id=dogonlanguages.__name__,
        name="Dogon and Bangime Linguistics",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://shh.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='dogonlanguages.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'}
    )
    DBSession.add(dataset)

    for c in util.CONTRIBUTORS:
        id_ = slug(c.name.split()[-1])
        data.add(models.Member, id_, id=id_, **attr.asdict(c))

    for i, spec in enumerate([
        ('heath', "Jeffrey Heath"),
        ('moran', "Steven Moran"),
    ]):
        DBSession.add(common.Editor(
            dataset=dataset,
            ord=i + 1,
            contributor=data['Member'][spec[0]]))

    url_resolver = util.UrlResolver(args)
    contrib = data.add(common.Contribution, 'd', id='d', name='Dogon Languages')
    project_docs = set()
    for rec in util.get_bib(args):
        obj = data.add(
            models.Document,
            rec.id,
            _obj=bibtex2source(rec, cls=models.Document))
        obj.project_doc = rec.get('keywords') == 'DLP'
        if obj.project_doc:
            for i, cid in enumerate(util.get_contributors(rec, data)):
                models.DocumentContributor(
                    document=obj, contributor=data['Member'][cid], ord=i)
        if obj.url:
            url = URL(obj.url)
            if url.host() == 'dogonlanguages.org':
                project_docs.add(url.path_segment(-1))
                res = url_resolver(rec['url'])
                if isinstance(res, dict):
                    obj.url = res['url']
                else:
                    obj.url = res

    print('got bib')
    #print(len(url_resolver.edmond_urls))
    #return

    for name, (gc, desc) in LANGUAGES.items():
        gl_lang = languoids[gc]
        lat, lon = gl_lang.latitude, gl_lang.longitude
        data.add(
            models.Languoid, gc,
            id=gc,
            name=name,
            description=desc,
            latitude=lat,
            longitude=lon,
            family=gl_lang.family.name if gl_lang and gl_lang.family else name,
        )

    print(len(village_images))
    contrib_by_initial = {c.abbr: c for c in data['Member'].values()}
    for lat, lon, d in util.gps(args):
        key = slug(d['OfficialVillageName'])
        if key not in data['Village']:
            if d['glottocode']:
                lang = data['Languoid'].get(d['glottocode'])
                if not lang:
                    gl_lang = languoids[d['glottocode']]
                    lang = data.add(
                        models.Languoid, gl_lang.id, id=gl_lang.id, name=gl_lang.name, in_project=False, family=gl_lang.family.name if gl_lang.family else gl_lang.name)
            else:
                lang = None
            village = data.add(
                models.Village, key,
                id=key,
                name=d['OfficialVillageName'],
                description=d['social info'],
                surnames=d['surnames'],
                major_city=d['MajorCity'] == 'Y',
                transcribed_name=d['Transcribed Village Name'],
                source_of_coordinates=d['sourceOfCoordinates'],
                latitude=lat,
                longitude=lon,
                languoid=lang,
                jsondata=d,
            )
            normname = d['OfficialVillageName'].replace('-', '').split('(')[0].strip()
            k = 0
            for n in village_images.keys()[:]:
                if '_%s_' % normname in n:
                    img = village_images[n]
                    mimetype = guess_type(img.path.name)[0]
                    if mimetype:
                        k += 1
                        f = models.Village_files(
                            id='%s-%s' % (key, k),
                            name=n,
                            description=img.description,
                            date_created=img.date,
                            latitude=img.coords[0] if img.coords else None,
                            longitude=-img.coords[1] if img.coords else None,
                            object=village,
                            mime_type=mimetype,
                        )
                        with img.path.open('rb') as fp:
                            f.create(args.data_file('files'), fp.read())
                        for initial in img.creators:
                            if initial in contrib_by_initial:
                                models.Fotographer(
                                    foto=f,
                                    contributor=contrib_by_initial[initial])

                    del village_images[n]
                    #else:
                    #    print('no image', normname)

    print(len(village_images))
    #return

    names = defaultdict(int)
    cids = {}
    for concept in reader(args.data_file('repos', 'fauna_Dogon_Unicode.csv'), delimiter=',', dicts=True):
        add(languoids, cids, util.ff_to_standard(concept), data, names, contrib, ff=True)

    for concept in reader(args.data_file('repos', 'dogon_lexicon.csv'), delimiter=',', escapechar='\\', namedtuples=True):
        add(languoids, cids, concept, data, names, contrib)

    ref_pattern = re.compile('(?P<ref>[0-9]{5})')
    count = 0
    for i, img in enumerate(reader(args.data_file('repos', 'dogon_flora-fauna.csv'), delimiter=',', namedtuples=True)):
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

    count = 0
    #for i, vid in enumerate(args.data_file('video', 'mp4').files('*.mp4')):
    #    match = ref_pattern.search(vid.basename())
    #    if match:
    #        ref = str(int(match.group('ref')))
    #        if ref in data['Concept']:
    #            concept = data['Concept'][ref]
    #            f = common.Parameter_files(
    #                object=concept,
    #                id=str(i + 1) + '.mp4',
    #                name=vid.basename(),
    #                mime_type='video/mp4')
    #            f.create(files_dir, open(vid, 'rb').read())
    #            count += 1
    #print count, 'videos detected'


def add(languoids, cids, concept, data, names, contrib, ff=False):
    domain = data['Domain'].get(concept.code)
    if domain is None:
        domain = data.add(
            models.Domain, concept.code,
            id=concept.code,
            name=concept.code_eng,
            description=concept.code_fr)
    scid = '-'.join([concept.code, concept.subcode.replace('.', '_')])
    subdomain = data['Subdomain'].get(scid)
    if subdomain is None:
        try:
            subdomain = data.add(
                models.Subdomain, scid,
                id=scid,
                name=concept.subcode_eng,
                description=concept.sous_code_fr,
                domain=domain)
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
            subdomain=subdomain)
        if ff:
            c.species = concept.species
            c.family = concept.family
    else:
        print '***', cid, concept.ref, concept.English
        return

    for i, (l, gc) in enumerate(LEX_LANGS):
        lang = data['Languoid'].get(gc)
        if lang is None:
            print(l)
            raise ValueError

        forms = (getattr(concept, l) or '').strip()
        if not forms:
            continue

        # FIXME: distinguish varieties as contributions!?
        vs = common.ValueSet(
            id='-'.join([cid, str(i + 1)]),
            language=lang,
            contribution=contrib,
            parameter=c)
        for j, form in enumerate(nfilter(util.split_words(forms))):
            v = models.Counterpart(
                id='-'.join([cid, str(i + 1), str(j + 1)]),
                valueset=vs,
                **util.parse_form(form))

    #
    # TODO: identify forms!
    #


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    sdata = jsonlib.load(args.data_file('repos', 'classification.json'))
    for species in DBSession.query(models.Concept).filter(models.Concept.ff == True):
        if species.id in sdata:
            util.update_species_data(species, sdata[species.id])


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
