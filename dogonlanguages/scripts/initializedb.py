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


def main(args):
    villages = util.get_villages(args)
    ff_images = list(util.ff_images(args))
    bib = list(util.get_bib(args))

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

    for i, id_ in enumerate(['heath', 'moran']):
        DBSession.add(common.Editor(
            dataset=dataset, ord=i + 1, contributor=data['Member'][id_]))

    contrib = data.add(common.Contribution, 'd', id='d', name='Dogon Languages')
    for doc in bib:
        obj = data.add(
            models.Document,
            doc.rec.id,
            _obj=bibtex2source(doc.rec, cls=models.Document))
        obj.project_doc = (doc.rec.get('keywords') == 'DLP') or bool(doc.files)
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
        data.add(
            models.Languoid, gc,
            id=gc,
            name=name,
            description=desc,
            latitude=lat,
            longitude=lon,
            family=gl_lang.family.name if gl_lang and gl_lang.family else name,
        )

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
        for j, img in enumerate(village.images):
            mimetype = guess_type(img.name)[0]
            if mimetype:
                f = models.Village_files(
                    id='%s-%s' % (v.id, j + 1),
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
    for concept in reader(args.data_file('repos', 'flora_Dogon_Unicode.csv'), delimiter=',', dicts=True):
        add(util.ff_to_standard(concept), data, names, contrib, ff=True)

    for concept in reader(args.data_file('repos', 'fauna_Dogon_Unicode.csv'), delimiter=',', dicts=True):
        add(util.ff_to_standard(concept), data, names, contrib, ff=True)

    for concept in reader(args.data_file('repos', 'dogon_lexicon.csv'), delimiter=',', escapechar='\\', namedtuples=True):
        add(concept, data, names, contrib)

    count = 0
    for i, img in enumerate(ff_images):
        if img.ref:
            if img.ref in data['Concept']:
                concept = data['Concept'][img.ref]
                common.Parameter_files(
                    object=concept,
                    id=str(i + 1),
                    name=img.name.decode('utf8'),
                    mime_type=guess_type(img.name)[0],
                    jsondata=img.cdstar)
                count += 1
            else:
                print('missing ref: %s' % img.ref)
    print(count, 'images detected')


def add(concept, data, names, contrib, ff=False):
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
            ff=ff,
            description=concept.Francais,
            subdomain=subdomain)
        if ff:
            c.species = concept.species
            c.family = concept.family
    else:
        assert cid == '50325'

    for i, (l, gc) in enumerate(LEX_LANGS):
        lang = data['Languoid'].get(gc)
        assert lang
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
            attrs = util.parse_form(form)
            if attrs['name'] and attrs['name'] != 'xxx':
                v = models.Counterpart(
                    id='-'.join([cid, str(i + 1), str(j + 1)]),
                    valueset=vs,
                    **util.parse_form(form))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    sdata = jsonlib.load(args.data_file('repos', 'classification.json'))
    for concept in DBSession.query(models.Concept).options(joinedload(common.Parameter._files)):
        for t_ in ['image', 'video']:
            setattr(concept, 'count_{0}s'.format(t_), len(getattr(concept, t_ + 's')))
        if concept.id in sdata:
            util.update_species_data(concept, sdata[concept.id])


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
