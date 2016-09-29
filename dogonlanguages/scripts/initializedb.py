from __future__ import unicode_literals
import sys
from collections import defaultdict
from mimetypes import guess_type

from sqlalchemy.orm import joinedload
import attr
from clldutils.dsv import reader
from clldutils.misc import slug, nfilter
from clldutils.path import Path
from clldutils import jsonlib

from clld.scripts.util import initializedb, Data, bibtex2source, add_language_codes
from clld.db.meta import DBSession
from clld.db.models import common
try:
    from pyglottolog.api import Glottolog
except ImportError:
    Glottolog = None

import dogonlanguages
from dogonlanguages import models
from dogonlanguages.scripts import util
from dogonlanguages.scripts.data import LANGUAGES


def main(args):
    for f in util.iter_files(args):
        DBSession.add(models.File(**attr.asdict(f)))

    lexicon = list(util.iter_lexicon(args))
    villages = util.get_villages(args)
    ff_images = list(util.ff_images(args))
    bib = list(util.get_bib(args))

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

    if Glottolog:
        glottolog = Glottolog(
            Path(dogonlanguages.__file__).parent.parent.parent.parent.joinpath(
                'glottolog3', 'glottolog'))
        languoids = {l.id: l for l in glottolog.languoids()}
    else:
        languoids = {}
    print('got glottolog')

    for c in util.CONTRIBUTORS:
        id_ = slug(c.name.split()[-1])
        data.add(models.Member, id_, id=id_, **attr.asdict(c))
    data.add(
        models.Member, 'forkel',
        id='forkel',
        name='Robert Forkel',
        email='forkel@shh.mpg.de',
        in_project=False)

    for i, id_ in enumerate(['moran', 'forkel', 'heath']):
        DBSession.add(common.Editor(
            dataset=dataset, ord=i + 1, contributor=data['Member'][id_]))

    contrib = data.add(common.Contribution, 'd', id='d', name='Dogon Languages')
    for doc in bib:
        obj = data.add(
            models.Document,
            doc.rec.id,
            _obj=bibtex2source(doc.rec, cls=models.Document))
        keywords = nfilter([s.strip() for s in doc.rec.get('keywords', '').split(',')])
        for dt in 'grammar lexicon typology texts'.split():
            if dt in keywords:
                obj.doctype = dt
                break
        obj.project_doc = ('DLP' in keywords) or bool(doc.files)
        if obj.project_doc:
            for i, cid in enumerate(util.get_contributors(doc.rec, data)):
                models.DocumentContributor(
                    document=obj, contributor=data['Member'][cid], ord=i)
        for i, (path, cdstar) in enumerate(doc.files):
            common.Source_files(
                id='%s-%s' % (obj.id, i + 1),
                name=path,
                object=obj,
                mime_type=guess_type(path)[0],
                jsondata=cdstar,
            )

    print('got bib')

    for name, (gc, desc) in LANGUAGES.items():
        gl_lang = languoids[gc]
        lat, lon = gl_lang.latitude, gl_lang.longitude
        lang = data.add(
            models.Languoid, gc,
            id=gc,
            name=name,
            description=desc,
            latitude=lat,
            longitude=lon,
            family=gl_lang.family.name if gl_lang and gl_lang.family else name,
        )
        if name == 'Penange' and lang.longitude > 0:
            lang.longitude = -lang.longitude
        if name == 'Bankan Tey':
            lang.latitude, lang.longitude = 15.07, -2.91
        if name == 'Ben Tey':
            lang.latitude, lang.longitude = 14.85, -2.95
        if name == 'Togo Kan':
            lang.latitude, lang.longitude = 14.00, -3.25
        add_language_codes(data, lang, gl_lang.iso, glottocode=gc)

    contrib_by_initial = {c.abbr: c for c in data['Member'].values()}
    for i, village in enumerate(villages):
        lang = None
        if village.glottocode:
            lang = data['Languoid'].get(village.glottocode)
            if not lang:
                gl_lang = languoids[village.glottocode]
                lang = data.add(
                    models.Languoid, gl_lang.id,
                    id=gl_lang.id,
                    name=gl_lang.name,
                    in_project=False,
                    family=gl_lang.family.name if gl_lang.family else gl_lang.name)
        v = data.add(
            models.Village, str(i + 1),
            id=str(i + 1),
            name=village.name,
            description=village.data.pop('social info'),
            surnames=village.data.pop('surnames'),
            major_city=village.data['MajorCity'] == 'Y',
            transcribed_name=village.data.pop('Transcribed Village Name'),
            source_of_coordinates=village.data.pop('sourceOfCoordinates'),
            latitude=village.lat,
            longitude=village.lon,
            languoid=lang,
            jsondata=village.data,
        )
        for img in village.images:
            mimetype = guess_type(img.name)[0]
            if mimetype:
                f = models.Village_files(
                    id=img.id,
                    name=img.name,
                    description=img.description,
                    date_created=img.date,
                    latitude=img.coords[0] if img.coords else None,
                    longitude=-img.coords[1] if img.coords else None,
                    object=v,
                    mime_type=mimetype,
                    jsondata=img.cdstar,
                )
                for initial in img.creators:
                    if initial in contrib_by_initial:
                        models.Fotographer(
                            foto=f, contributor=contrib_by_initial[initial])

    names = defaultdict(int)
    for concept in lexicon:
        add(concept, data, names, contrib)

    count = set()
    for img in ff_images:
        if img.id in count:
            continue
        count.add(img.id)
        if img.ref:
            if img.ref in data['Concept']:
                concept = data['Concept'][img.ref]
                if img.tsammalex_taxon and not concept.tsammalex_taxon:
                    concept.tsammalex_taxon = img.tsammalex_taxon
                    #print(concept.tsammalex_taxon)
                common.Parameter_files(
                    object=concept,
                    id=img.id,
                    name=img.name.decode('utf8'),
                    mime_type=guess_type(img.name)[0],
                    jsondata=img.cdstar)
            else:
                print('missing ref: %s' % img.ref)


def add(concept, data, names, contrib):
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
        subdomain = data.add(
            models.Subdomain, scid,
            id=scid,
            name=concept.subcode_eng,
            description=concept.sous_code_fr,
            domain=domain)

    cid = '%05d' % int(concept.ref)
    if concept.English in names:
        name = '%s (%s)' % (concept.English, names[concept.English] + 1)
    else:
        name = concept.English
    names[concept.English] += 1

    c = data['Concept'].get(cid)
    if c is None:
        c = data.add(
            models.Concept, cid,
            core=concept.core == '1',
            id=cid,
            name=name,
            description=concept.Francais,
            subdomain=subdomain,
            jsondata=dict(ref='%s-%s-%s' % (concept.code, concept.subcode, concept.subsubcode)))
        if concept.species:
            c.species = concept.species
        if concept.family:
            c.family = concept.family
    else:
        assert cid == '50325'

    for gc, forms in concept.forms.items():
        lang = data['Languoid'].get(gc)
        assert lang
        if not forms:
            continue

        vs = common.ValueSet(
            id='-'.join([cid, gc]),
            language=lang,
            contribution=contrib,
            parameter=c)
        for j, form in enumerate(nfilter(util.split_words(forms))):
            attrs = util.parse_form(form)
            if attrs['name'] and attrs['name'] != 'xxx':
                models.Counterpart(
                    id='-'.join([vs.id, str(j + 1)]),
                    valueset=vs,
                    **util.parse_form(form))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    concepticon = {
        c.GLOSS: c.CONCEPTICON_ID for c in
        reader(args.data_file('repos', 'conceptlist.tsv'), delimiter='\t', namedtuples=True)
        if c.CONCEPTICON_ID}
    sdata = jsonlib.load(args.data_file('repos', 'classification.json'))
    for concept in DBSession.query(models.Concept).options(joinedload(common.Parameter._files)):
        for t_ in ['image', 'video']:
            setattr(concept, 'count_{0}s'.format(t_), len(getattr(concept, t_ + 's')))
        if concept.jsondata['ref'] in sdata:
            util.update_species_data(concept, sdata[concept.jsondata['ref']])
        if concept.name in concepticon:
            concept.concepticon_id = int(concepticon[concept.name])


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
