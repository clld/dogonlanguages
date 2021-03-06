# coding=utf8
from __future__ import unicode_literals, print_function
import re
from hashlib import md5
from collections import defaultdict
from mimetypes import guess_type
from datetime import date

from purl import URL
import attr
from fuzzywuzzy import fuzz
from clldutils.dsv import reader
from clldutils.path import Path
from clldutils.jsonlib import load

from clld.lib.bibtex import Record, Database, unescape

from dogonlanguages.scripts.data import GPS_LANGS, FIELD_MAP, LEX_LANGS


@attr.s
class File(object):
    id = attr.ib()
    name = attr.ib()
    mime_type = attr.ib()
    date_created = attr.ib()
    size = attr.ib()
    duration = attr.ib()
    jsondata = attr.ib()


date_p = re.compile('_(?P<m>(0|1)[0-9])_((?P<d>[0-3][0-9])_)?(?P<y>(1|2)[0-9]{3})_')


def iter_files(args):
    files = defaultdict(list)
    for n in """
        Burkina_flora_for_website.json
        data.json
        docs.json
        edmond.json
        ffmissing.json
        Heath_flora_fauna_images.json
        Mali_villages_with_coordinates_for_website.json
        texts.json
        videos_from_website.json
        videos.json
    """.split():
        files.update(load(args.data_file('repos', n)))
    missing, matched = 0, 0
    for md5, cdstar in load(args.data_file('repos', 'cdstar.json')).items():
        if md5 in files:
            fnames = [Path(p.encode('utf8')).name.decode('utf8') for p in files[md5]]
            fname = sorted(fnames, key=lambda n: len(n))[-1]
            fname = fname.replace(' ', '_')
            if fname == 'Thumbs.db':
                continue
            m = date_p.search(fname)
            if m:
                d = date(int(m.group('y')), int(m.group('m')), int(m.group('d') or 1))
            else:
                d = None
            yield File(
                md5,
                fname,
                guess_type(fname)[0].decode('utf8'),
                d,
                cdstar['size'],
                cdstar.get('duration'),
                cdstar)
            matched += 1
        else:
            missing += 1
    print('iter_files', missing, matched)


def get_contributors(rec, data):
    for author in re.split('\s+and\s+', unescape(rec['author'])):
        for cid, obj in data['Member'].items():
            if fuzz.token_sort_ratio(author, obj.name) >= 92:
                yield cid


def update_species_data(species, d):
    eol = d.get('eol')
    if eol:
        species.update_jsondata(eol_id=eol['identifier'])


def split_words(s):
    """
    split string at , or ; if this is not within brackets.
    """
    s = re.sub('\s+', ' ', s)
    chunk = ''
    in_bracket = False

    for c in s:
        if c in ['(', '[']:
            in_bracket = True
        if c in [')', ']']:
            in_bracket = False
        if c in [',', ';'] and not in_bracket:
            yield chunk
            chunk = ''
        else:
            chunk += c
    if chunk:
        yield chunk


def parse_form(form):
    form = form.strip()
    attrs = {}
    parts = form.split('(', 1)
    if len(parts) == 2:
        attrs['name'] = parts[0].strip()
        if not parts[1].endswith(')'):
            if parts[1].endswith('"'):
                parts[1] += ')'
            else:
                #print(form, '->', parts[1])
                return {'name': form}
        comment = parts[1][:-1].strip()
        if comment.startswith('"') and comment.endswith('"'):
            attrs['description'] = comment[1:-1].strip()
        else:
            attrs['comment'] = comment
    else:
        attrs['name'] = form
    return attrs


KV_PATTERN = re.compile('(?P<key>[A-Za-z]+)\s*\=\s*\{(?P<value>.*)$', re.MULTILINE)


def fixed(mess):
    id_ = md5('@'.encode('utf8') + mess.encode('utf8'))
    for messyid in ['BibTeX', 'Indiana University']:
        mess = mess.replace(messyid + ',\n', '')
    genre, rem = mess.split('{', 1)
    assert rem.endswith('}')
    rem = rem[:-1].strip()
    kw = {}
    for kv in re.split('},\n', rem):
        kv = kv.strip()
        if kv.endswith('}'):
            kv = kv[:-1]
        m = KV_PATTERN.match(kv)
        if not m:
            #print kv
            continue
        if m.group('value').strip():
            kw[m.group('key').lower()] = m.group('value').strip()
    if kw:
        return Record(genre, id_.hexdigest().decode('ascii'), **kw)


@attr.s
class Document(object):
    rec = attr.ib()
    files = attr.ib(default=attr.Factory(list))


def get_bib(args):
    uploaded = load(args.data_file('repos', 'cdstar.json'))
    fname_to_cdstar = {}
    for type_ in ['texts', 'docs', 'data']:
        for hash_, paths in load(args.data_file('repos', type_ + '.json')).items():
            if hash_ in uploaded:
                for path in paths:
                    fname_to_cdstar[path.split('/')[-1]] = uploaded[hash_]
    for hash_, paths in load(args.data_file('repos', 'edmond.json')).items():
        if hash_ in uploaded:
            for path in paths:
                fname_to_cdstar[path.split('/')[-1]] = uploaded[hash_]
    db = Database.from_file(args.data_file('repos', 'Dogon.bib'), lowercase=True)
    for rec in db:
        doc = Document(rec)
        newurls = []
        for url in rec.get('url', '').split(';'):
            if not url.strip():
                continue
            if url.endswith('sequence=1'):
                newurls.append(url)
                continue
            url = URL(url.strip())
            if url.host() in ['dogonlanguages.org', 'github.com', '']:
                fname = url.path().split('/')[-1]
                doc.files.append((fname, fname_to_cdstar[fname]))
            else:
                newurls.append(url.as_string())
        doc.rec['url'] = '; '.join(newurls)
        yield doc


@attr.s
class Contributor(object):
    name = attr.ib()
    description = attr.ib()
    email = attr.ib()
    url = attr.ib()
    abbr = attr.ib()

CONTRIBUTORS = [
    Contributor(
        "Minkailou Djiguiba",
        """Minkailou is a native speaker of Jamsay (Dogon), and also speaks French, Fulfulde, and Bambara. After graduating from secretariat school at IFN in Sevare, he joined the project initially as Jamsay informant and assistant for Heath. He has stayed on as a full-time employee to manage our bases and to organize our travels and our visits to Dogon villages. He has filmed some of our feature videos and has done much work in the geography and flora-fauna components of the project. He drives the project vehicle (which he owns).""",
        "minkailoudjiguiba (at) yahoo.fr",
        None,
        'MD'),
    Contributor(
        "Vadim Dyachkov",
        """Vadim is a postgraduate student of the Moscow State University, and works at the Russian Academy of Science. He studies linguistics focusing on morphology, syntax and their interactions, especially on deadjectival verb typology and the theory of subjecthood. He joined the project in 2011. He has made four trips to Mali (and Burkina) beginning in 2011. He has focused on the Tomo Kan dialect spoken in Segue, and is working on a grammar and a dictionary.""",
        "hyppocentaurus (at) mail.ru",
        None,
        'VD'),
    Contributor(
        "Stefan Elders",
        """Stefan was a Dutch post-doc trained at University of Leiden (Netherlands) and active as a research associate at the University of Bayreuth (Germany), joined the project in September 2006 to work on Bangime in the village of Bounou. His tragic death in Mali due to a sudden illness in February 2007 was a devastating blow to West African linguistics. In his short career he did extensive fieldwork in Cameroon and Burkina Faso, made important contributions to Gur and West Atlantic linguistics, and was in the process of becoming one of the major overall authorities on West African linguistics. This website presents the materials we were able to salvage from his work on Bangime: a handout he prepared for a workshop on Dogon languages in Bamako December 2006, and scans from his notebooks (courtesy of the Elders family). The original notebooks are archived at the University of Leiden library. We are also in possession of two partially recorded cassettes, some flora specimens, and a number of ethnographic photographs that we will process and disseminate. Click on the Bangime tab for more on Elders' work on this language.""",
        None,
        None,
        'SE'),
    Contributor(
        "Abbie Hantgan",
        """Abbie, then a graduate student in Linguistics at Indiana University, was recruited following Elders' death to carry on the study of Bangime. She had previously been a Peace Corps volunteer in Mali for several years, based initially in the village of Koira Beiri (Kindige language area) and then in Mopti-Sevare. She is fluent in Fulfulde, which is invaluable as a lingua franca in the Bangime villages, and has recently learned to speak Bambara/Jula. Abbie did initial fieldwork on Bangime in Bounou June-August 2008, and has returned to the field several times since. Her 2013 PhD dissertation was a description and analysis of aspects of the phonology, morphology, and morphosyntax of Bangime. She has also worked on Ibi So, and has published on the Kindige ATR system. She is currently a postdoctoral fellow at SOAS in London, on the Leverhulme funded Crossroads Project focusing on multilingualism among Senegalese languages.""",
        "ahantgan (at) umail.iu.edu",
        "https://soascrossroads.org/team/post-doc-research-fellows/abbie-hantgan/",
        'AH'),
        #(includes a grammar and lexicon of Tiefo, a severely endangered Gur language of SW Burkina Faso)
        #Abbie's article in the Returned Peace Corps Volunteer Newsletter [pdf]
    Contributor(
        "Jeffrey Heath",
        """Jeff is Prof. of Linguistics, University of Michigan (Ann Arbor), and is a veteran of more than 14 years of on-location fieldwork. He began with Australian Aboriginal languages of eastern Arnhem Land (1970's), then did various topical projects on Jewish and Muslim dialects of Maghrebi Arabic (1980's). Since 1989 he has made annual trips to Mali where he has worked in succession on Hassaniya Arabic, riverine Songhay languages (Koyra Chiini, Koyraboro Senni), montane Songhay languages (Tondi Songway Kiini, Humburi Senni), and Tamashek (Berber family). Since 2005 he has focused on Dogon languages: Jamsay, Ben Tey, Bankan Tey, Bunoge, Najamba, Nanga, Penange, Tebul Ure, Tiranige, Yanda Dom, Donno So, and Dogul Dom. During his 2011-12 fieldwork stint he has also been shooting and producing low-budget videos of cultural events and everyday practical activities, some of which can be viewed on the project website. He has also been mapping Dogon villages in collaboration with the LLMAP project at Eastern Michigan University, and has continued to work on local flora-fauna and native terms thereof. He is the author of A Grammar of Jamsay (Mouton, 2008), but his more recent Dogon grammars are currently disseminated on the project website or published in the open-access Language Description Heritage Library and permanently archived at Deep Blue at the University of Michigan. In Burkina, Jeff is working on Tiefo (Gur) in collaboration with others, and on Jalkunan (Mande).""",
        "schweinehaxen (at) hotmail.com",
        "http://www-personal.umich.edu/~jheath/",
        'JH'),
    Contributor(
        "Laura McPherson",
        """Laura is an assistant professor in the Linguistics Program at Dartmouth College. Her main theoretical interests are in phonology, tonology, and the phonology-syntax interface. She earned her BA in Linguistics from Scripps College in 2008, working with Africanist Mary Paster on the verbal morphology of Luganda, and her PhD from UCLA in 2014 with the dissertation Replacive grammatical tone in the Dogon languages (co-chairs Bruce Hayes and Russell Schuh). She spent eleven months in Mali on her first field trip (2008-2009) working on Tommo So, first with the support of our project then with the support of a Fulbright Fellowship. She returned to Mali annually to continue work and published A Grammar of Tommo So in the Mouton Grammar Library in 2013. She has more recently shifted focus to Seenku, a Mande language of Burkina Faso, and to languages of Melanesia.""",
        "laura.emcpherson (at) gmail.com",
        "http://www.dartmouth.edu/~mcpherson/",
        'LM'),
    Contributor(
        "Steven Moran",
        """Steve is a veteran of the Eastern Michigan University Linguist List and E-MELD team and went on to get a 2012 Ph.D. in Computational Linguistics at the University of Washington with a dissertation title "Phonetics information base and lexicon." He previously did fieldwork in Ghana and published a grammatical sketch of Western Sisaala. He manages the Dogon project website, and has done fieldwork on Toro-So (Sangha So dialect) in 2009 and 2013. He was a postdoc researcher at the University of Munich (Germany) in the project "Quantitative language comparison" funded by the European Research Council from 2012-2014, and is currently a postdoc in the Department of Comparative Linguistics at the University of Zurich. """,
        "bambooforest (at) gmail.com",
        "http://www.comparativelinguistics.uzh.ch/de/moran.html",
        'SM'),
    Contributor(
        "Kirill Prokhorov",
        """Kirill is a Russian Ph.D. who has been trained by West African specialists and field-oriented typologists in Moscow and St. Petersburg. Since 2008 he has focused on the Mombo (also known as Kolu-So) language with a base in the picturesque village of Songho just west of Bandiagara. In January 2009 he was a visiting scholar for one month at the Max Planck Institute for Evolutionary Anthropology (MPI-EVA) in Leipzig, which also provided him with a stipend to support his 2008 fieldwork. He has made return trips to Dogon country in 2009, 2010 and 2011. He has also studied Ampari, and did short pilot-studies of Bunoge and Penange. From 2010 to 2014 he was based at Humboldt University (Berlin) where he worked on the project "Predicate-centered focus types: A sample-based typological study in African languages", part of the larger project SFB 632 "Information Structure" funded by German Science Association (DFG).""",
        "bolshoypro (at) gmail.com",
        None,
        'KP'),
    Contributor(
        "Vu Truong",
        """Vu graduated from Brandeis University with a B.A. in linguistics in 2011. In 2010, he designed and implemented a sociolinguistic survey in Sokone, Senegal on attitudes towards language shift to Wolof. In 2011, he taught English in Kagoshima, Japan as part of the JET Program. He joined the project in August 2012. He was at our base in Bobo Dioulasso from mid-2012 to mid-2014, working on the Jalkunan language (Mande family, about 500 speakers). He is now a student in the Linguistics PhD program at the University of Chicago.""",
        "finath (at) gmail.com",
        None,
        'VT'),
]


class Entry(object):
    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)
        self.forms = {}


def iter_lexicon(args):
    for fname in ['dogon_lexicon', 'flora_Dogon_Unicode', 'fauna_Dogon_Unicode']:
        for concept in reader(args.data_file('repos', fname + '.csv'), dicts=True):
            entry = Entry(**{v: concept.get(k) for k, v in FIELD_MAP.items()})
            for name, gc in LEX_LANGS[fname].items():
                entry.forms[gc] = concept[name].strip()
            if entry.ref and entry.ref != 'zzz':
                yield entry


@attr.s
class FFImage(object):
    id = attr.ib()
    name = attr.ib()
    description = attr.ib()
    ref = attr.ib()
    date = attr.ib()
    creators = attr.ib()
    cdstar = attr.ib()
    tsammalex_taxon = attr.ib()


def ff_images(args):
    tsammalex = {
        i.id: i.taxa__id for i in
        reader(args.data_file('repos', 'tsammalex_images.csv'), namedtuples=True)}

    ref_pattern = re.compile('(?P<ref>[0-9]{5})')
    uploaded = load(args.data_file('repos', 'cdstar.json'))
    files = load(args.data_file('repos', 'Heath_flora_fauna_images.json'))
    files.update(load(args.data_file('repos', 'ffmissing.json')))
    path_to_md5 = {}
    for md5, paths in files.items():
        for path in paths:
            path_to_md5[Path(path.encode('utf8')).stem] = md5
    missed, found, uploaded_ = 0, 0, 0
    for i, img in enumerate(reader(args.data_file('repos', 'dogon_flora-fauna.csv'), delimiter=',', namedtuples=True)):
        stem = Path(img.filenames.encode('utf8')).stem
        assert stem in path_to_md5
        found += 1
        if path_to_md5[stem] in uploaded:
            m = ref_pattern.search(stem)
            uploaded_ += 1
            yield FFImage(
                path_to_md5[stem],
                Path(files[path_to_md5[stem]][0].encode('utf8')).name,
                None,
                m.group('ref') if m else None,
                None,
                [],
                uploaded[path_to_md5[stem]],
                tsammalex.get(path_to_md5[stem]))

    videos = load(args.data_file('repos', 'videos_from_website.json'))
    videos.update(load(args.data_file('repos', 'videos.json')))

    for md5, paths in videos.items():
        if md5 in uploaded:
            path = Path(paths[0].encode('utf8'))
            m = ref_pattern.search(path.stem)
            uploaded_ += 1
            yield FFImage(
                md5,
                path.name,
                None,
                m.group('ref') if m else None,
                None,
                [],
                uploaded[md5],
                tsammalex.get(md5))
        else:
            missed += 1

    print('ff_images', missed, uploaded_)


@attr.s
class VillageImage(object):
    id = attr.ib()
    name = attr.ib()
    village = attr.ib()
    description = attr.ib()
    date = attr.ib()
    creators = attr.ib()
    coords = attr.ib()
    cdstar = attr.ib()


VFN = {
    'Qcoord;5digit_Dogon_Jamsay_Yangassadiou_near_Mondoro_ph1_MD_JH.JPG': '',
    'P1010666_DonnoSo_Tognon_upper_06_2014.JPG': 'Tongnon',
    'Fulfulde_Sosari_aka_Sassari_70105_N14_35_W03_54_village_03_2012_MD_JH.JPG': 'Soosari',
    'P1010668_DonnoSo_Wendeguele_06_2014.JPG': 'Wendegele',
    'Qname_Dogon_TebulUre_village_below2_05_2009_JH.JPG': '',
    'Qcoord;5digit_Dogon_Jamsay_DianwelyPomidori_03_2011_SM_JH.JPG': '',
    'Dogon_TommoSo_Goundioli_70585_N14_36_W03_21_village_01_2011_JH.JPG': 'Goundoli',
    'Qname_Dogon_TebulUre_hilltop_village_06_2009_JH.JPG': '',
    'Qcoord;5digit_Dogon_NajambaKindige;Kindige_Bal_near_Dogani_10_2011_JH.JPG': '',
    'Qcoord;5digit_Dogon_Jamsay_Yangassadiou_near_Mondoro_ph3_MD_JH.JPG': '',
    'Qcoord_Fulfulde_WouroToroli_05_2011_JH.JPG': 'Ouro-Toroli',
    'Qname_Dogon_TebulUre_village_below1_05_2009_JH.JPG': '',
    'Qcoord;5digit_Dogon_Jamsay_Yangassadiou_near_Mondoro_ph2_MD_JH.JPG': '',
    'Qcoord;5digit_Dogon_ToroTegu_Newri_XXX_abandoned_village_shadowed_area_in_center_near_Youna_03_2011_JH.JPG': '',
    'P1010667_DonnoSo_Tognon_lower_06_2014.JPG': 'Tongnon',
    'Qcoord;5digit_Dogon_NajambaKindigue;Kindigue_Bal_near_Dogani_10_2011_JH.JPG': '',
    'Qwhichvillage_Songhay_HS_DakaKouko_XXX_06_2011_JH.JPG': 'Daka-Kuko',
    'Qname_Dogon_TebulUre_village_at_base_of_rocks_06_2009_JH.JPG': '',
    'Qname_Dogon_TebulUre_village_on_slope_in_rocks_05_2009_JH.JPG': '',
}


def village_images(args):
    uploaded = load(args.data_file('repos', 'cdstar.json'))
    files = load(
        args.data_file('repos', 'Mali_villages_with_coordinates_for_website.json'))
    for hash_, paths in files.items():
        if hash_ in uploaded:
            fname = Path(paths[0])
            name, coords, desc, date_, creators = image_md(fname.stem)
            yield VillageImage(hash_, fname.name.decode('utf8'), VFN.get(fname.name), desc, date_, creators, coords, uploaded[hash_])


def parse_deg(s):
    if s:
        try:
            deg, min = s.split()
            return float(deg) + (float(min) / 60)
        except:
            comps = s.split('.')
            if len(comps) == 3:
                deg, min = comps[0], '.'.join(comps[1:])
                return float(deg) + (float(min) / 60)
            else:
                if s not in ['0', 'see Ogourou']:
                    raise ValueError
            return


ID_PATTERN = re.compile('_([0-9]{5})_')
COORDS_PATTERN = re.compile('(N[0-9]{2}_[0-9]{2}\+?_W[0-9]{2}_[0-9]{2})')
DATE_PATTERN = re.compile('((?:_?[0-9]{2})?_[0-9]{4})(?:_|$)')
INITIALS_PATTERN = re.compile('((?:_[A-Z]{2})+)$')


def image_md(name):
    """
    Dogon_Nanga_Anda_70371_N14_49_W03_01_village_from_above_03_2011_SM_JH.JPG
    """
    def totext(s):
        if s:
            return s.replace('_', ' ').strip()

    def todate(s):
        if s:
            s = totext(s).split()
            if len(s) == 2:
                d, m, y = 1, int(s[0]), int(s[1])
            else:
                d, m, y = 1, 1, int(s[0])
            return date(y, m, d)

    def tolatlon(s):
        return map(parse_deg, s[1:].replace('+', '').replace('_', ' ').split('W'))

    name = name.replace('.', '_').replace(' ', '_')
    coords, date_, lang_and_name = None, None, None
    if ID_PATTERN.search(name):
        lang_and_name, _, rem = ID_PATTERN.split(name)
    else:
        rem = name
    if COORDS_PATTERN.search(rem):
        _, coords, rem = COORDS_PATTERN.split(rem)
        coords = tolatlon(coords)
        if not lang_and_name:
            lang_and_name = _
    if DATE_PATTERN.search(rem):
        desc, date_, rem = DATE_PATTERN.split(rem, maxsplit=1)
    else:
        if INITIALS_PATTERN.search(rem):
            desc, rem, _ = INITIALS_PATTERN.split(rem)
        else:
            desc, rem = rem, ''
    return totext(lang_and_name), coords, totext(desc), todate(date_), (totext(rem) or '').split()


@attr.s
class Village(object):
    name = attr.ib()
    normname = attr.ib()
    glottocode = attr.ib()
    data = attr.ib()
    lat = attr.ib(default=0)
    lon = attr.ib(default=0)
    images = attr.ib(default=attr.Factory(list))


def gps(args):
    """
    Multilingual,
    lg family, -> Dogon, Atlantic, Mande, Berber, ...
    family code ,
    Language (group), -> Names of Dogon languages
    alternate lg (group), -> comma separated list of language names
    language code, -> ISO 639-3
    Language (based on native name),
    dialect code,
    ISO 3 Letter country code,
    OfficialVillageName, -> name!
    MajorCity,
    PopulationNumber,
    village (RB),
    village (DNAFLA),
    village (SIL),
    village (map), -> alternative name
    Transcribed Village Name, -> keep
    N Lat,
    W Lon,
    NFr,
    WFr,
    Nmn60,
    Wmn60,
    NMinFr,
    WMinFr,
    Ndg,
    Wdg,
    N Lat_2, -> 12 12.123
    W Lon_2, -> 12 12.123
    N SIL,
    W SIL,
    N Lat source,
    WLon source,
    N Lat map,
    WLon map,
    N Lat us,
    W Long us,
    sourceOfCoordinates, -> keep
    name of map, -> keep
    lg comment, -> keep
    industries, -> keep
    weekly market, -> keep
    surnames, -> keep
    social info, -> keep
    Image,
    ImageDescription,
    Audio,
    AudioTranscription,
    Video,
    VideoTranscription
    """
    full_name_map = {
        'Oualo (upper)': 'walo_upper',
        'Oualo (lower)': 'walo_lower',
        'Kenntaba-Leye': 'kentabaley',
        'Djimerou-Doungo': 'djimeroudungo',
        'Sassourou': 'sassouru',
        'Sege-Bougie': 'seguebougie',
        'Fiko': 'ficko',
        'Iribanga (Fulbe)': 'iribanga_fulbe',
        'Madina (near Banggel-Toupe)': 'madina_near_bangueltoupe)',
        'Dourou Tanga (1)': 'douroutanga_1',
        'Dourou Tanga (2)': 'douroutanga_2',
        'Dourou Tanga (3)': 'douroutanga_3',
        'Tena (Tere)': 'tena_aka_tere',
        'Anakaga (Amamounou)': 'anakaga_in_amamounou',
        'Dari (near Hombori)': 'dari_near_hombori',
        'Bamba Tene': 'bambatende',
        'Kenntaba-Do': 'kentabado',
        'Tialegel': 'tialeggel',
        'Bani-Banggou': 'banibangou',
        'Ourobangourdi': 'ourobaangourdi',
        'Ourodjougal': 'ourodiouggal',
        'Yadianga (Fulbe)': 'yadiangapoulogoro',
        'Gueourou (Fulbe)': 'gueouroupulogoro',
        'Tongoro-Legu': 'tongorolegou',
        'Koundougou-Mossi': 'koundougoumouniougoro',
        'Billanto-Bella': 'bella',
        'Dianggassagou (Diemessogou)': 'diangassagou_aka_diemessogou)',
    }
    name_map = {
        'kelmita': 'kelmitaa',
        'yrebann': 'yreban',
        'aouguine': 'aougine',
        'bendielysigen': 'bendielisigen',
        'bendielydana': 'bendielidana',
        'ourongeou': 'ourongueou',
        'oukoulourou': 'oukolourou',
        'bendielygirikombo': 'bendieligirikombo',
        'dianggassagou': 'diangassagou',
        'komokanina': 'komokaninaa',
        'dourouna': 'dourounaa',
        'idielina': 'idielinaa',
        'woltigueri': 'woltiguere',
        'irelikanaw': 'ireli_kanaw',
        'korimaounde': 'kori_maounde',
        'yandaguinedia': 'yandaginedia',
        'boudoufolii': 'boudoufoli_section1',
        'boudoufoliii': 'boudoufoli_section2',
    }

    def location(d):
        if d['OfficialVillageName'] == 'Balaguina (Balaguina-Baboye)':
            d['N Lat'] = d['N Lat'].replace(' 115.3', ' 15.3')
        if d['OfficialVillageName'] == 'Daidourou':
            return None, None
        #if d['W Lon us'] and d['N Lat us']:
        #    return parse_deg(d['N Lat us']), parse_deg(d['W Lon us'])
        lat, lon = parse_deg(d['N Lat']), parse_deg(d['W Lon'])
        if lon:
            lon = -lon
        if lon and lon < -10:
            lon += 10
        return lat, lon

    for d in reader(
            args.data_file('repos', 'GPS_Dogon.csv'), dicts=True):
        for k in d:
            d[k] = d[k].strip()
        if not d['OfficialVillageName']:
            continue
        normname = full_name_map.get(d['OfficialVillageName'].strip())
        if normname is None:
            normname = d['OfficialVillageName'].replace('-', '').replace(' ', '').replace('(', '_aka_').replace(')', '').split(',')[0].strip().lower()
            normname = name_map.get(normname, normname)
        v = Village(
            d['OfficialVillageName'],
            normname,
            GPS_LANGS.get(d['Language (group)']),
            data=d)
        v.lat, v.lon = location(d)
        yield v


def get_villages(args):
    villages = sorted(list(gps(args)), key=lambda v: -len(v.normname))
    for img in village_images(args):
        imgname = img.name.lower()
        for v in villages:
            comp = imgname
            if '_near_' not in v.normname:
                comp = comp.split('_near_')[0] + '_'

            if '_%s_' % v.normname in comp or (img.village and img.village == v.name):
                v.images.append(img)
                break
        else:
            for v in villages:
                if '_aka_' in v.normname:
                    comp = imgname
                    if '_near_' not in v.normname:
                        comp = comp.split('_near_')[0] + '_'

                    if '_%s_' % v.normname.split('_aka_')[0] in comp:
                        v.images.append(img)
                        break
            else:
                print('get_villages - not matched: %s' % img.name)
    return villages
