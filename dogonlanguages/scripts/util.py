# coding=utf8
from __future__ import unicode_literals
import re
from hashlib import md5
from io import open
import shutil
from collections import defaultdict
from subprocess import check_output
from urllib import urlretrieve

import requests
from fuzzywuzzy import fuzz
from purl import URL

from clld.lib.imeji import file_urls
from clld.lib.bibtex import Record, Database, unescape


def get_contributors(rec, data):
    for author in re.split('\s+and\s+', unescape(rec['author'])):
        for cid, obj in data['Contributor'].items():
            if fuzz.token_sort_ratio(author, obj.name) >= 92:
                yield cid


class UrlResolver(object):
    def __init__(self, args):
        self.args = args
        self.checksums = {}
        if not args.data_file('docs').exists():
            self.edmond_urls = {}
        else:
            for fname in args.data_file('docs').iterdir():
                if fname.is_file():
                    self.checksums[fname.name] = check_output(
                        'md5sum "%s"' % fname.as_posix().decode('utf8'), shell=True).split()[0]
            for fname in args.data_file('docs', 'not_on_edmond').iterdir():
                if fname.is_file():
                    self.checksums[fname.name] = check_output(
                        'md5sum "%s"' % fname.as_posix().decode('utf8'), shell=True).split()[0]
            self.edmond_urls = {d['md5']: d for d in file_urls(args.data_file('Edmond.xml').as_posix())}

    def __call__(self, url_):
        url = URL(url_)
        if url.host() == 'dogonlanguages.org':
            basename = url.path_segment(-1)
            if basename in self.checksums:
                checksum = self.checksums[basename]
                if checksum in self.edmond_urls:
                    return self.edmond_urls[checksum]
        return url_


def update_species_data(species, d):
    eol = d.get('eol')
    if eol:
        for an in eol.get('ancestors', []):
            if not an.get('taxonRank'):
                continue
            for tr in ['family']:
                if tr == an['taxonRank']:
                    curr = getattr(species, tr)
                    #if curr != an['scientificName']:
                    #print(tr, ':', curr, '-->', an['scientificName'])
                        #setattr(species, tr, an['scientificName'])

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
    attrs = {}
    parts = form.split('(', 1)
    if len(parts) == 2:
        attrs['name'] = parts[0].strip()
        if not parts[1].endswith(')'):
            if parts[1].endswith('"'):
                parts[1] += ')'
            else:
                print '---->', parts[1]
                return {'name': form}
        comment = parts[1][:-1].strip()
        if comment.startswith('"') and comment.endswith('"'):
            attrs['description'] = comment[1:-1].strip()
        else:
            attrs['comment'] = comment
    else:
        attrs['name'] = form
    return attrs


def get_thumbnail(args, filename):
    path = args.data_file('repos', 'thumbnails', filename.encode('utf8'))
    if not path.exists():
        print path
        return
        r = requests.get('http://dogonlanguages.org/thumbnails/' + filename, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            return
    with open(path.as_posix(), 'rb') as f:
        return f.read()


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


def get_bib(args):
    db = Database.from_file(args.data_file('repos', 'Dogon.bib'), lowercase=True)
    keys = defaultdict(int)
    for rec in db:
        keys[rec.id] += 1
        rec.id = '%sx%s' % (rec.id, keys[rec.id])
        yield rec


CONTRIBUTORS = {
    "Minkailou Djiguiba": ("""is a native speaker of Jamsay (Dogon), and also speaks French, Fulfulde, and Bambara. After graduating from secretariat school at IFN in Sevare, he joined the project initially as Jamsay informant and assistant for Heath. He has stayed on as a full-time employee to manage our bases and to organize our travels and our visits to Dogon villages. He has filmed some of our feature videos and has done much work in the geography and flora-fauna components of the project. He drives the project vehicle (which he owns).""",
        "minkailoudjiguiba (at) yahoo.fr",
        None),

    "Vadim Dyachkov": ("""is a postgraduate student of the Moscow State University, and works at the Russian Academy of Science. He studies linguistics focusing on morphology, syntax and their interactions, especially on deadjectival verb typology and the theory of subjecthood. He joined the project in 2011. He has made four trips to Mali (and Burkina) beginning in 2011. He has focused on the Tomo Kan dialect spoken in Segue, and is working on a grammar and a dictionary.""",
        "hyppocentaurus (at) mail.ru",
        None),

    "Stefan Elders": ("""a Dutch post-doc trained at University of Leiden (Netherlands) and active as a research associate at the University of Bayreuth (Germany), joined the project in September 2006 to work on Bangime in the village of Bounou. His tragic death in Mali due to a sudden illness in February 2007 was a devastating blow to West African linguistics. In his short career he did extensive fieldwork in Cameroon and Burkina Faso, made important contributions to Gur and West Atlantic linguistics, and was in the process of becoming one of the major overall authorities on West African linguistics. This website presents the materials we were able to salvage from his work on Bangime: a handout he prepared for a workshop on Dogon languages in Bamako December 2006, and scans from his notebooks (courtesy of the Elders family). The original notebooks are archived at the University of Leiden library. We are also in possession of two partially recorded cassettes, some flora specimens, and a number of ethnographic photographs that we will process and disseminate. Click on the Bangime tab for more on Elders' work on this language.""",
        None, None),

    "Abbie Hantgan": ("""then a graduate student in Linguistics at Indiana University, was recruited following Elders' death to carry on the study of Bangime. She had previously been a Peace Corps volunteer in Mali for several years, based initially in the village of Koira Beiri (Kindige language area) and then in Mopti-Sevare. She is fluent in Fulfulde, which is invaluable as a lingua franca in the Bangime villages, and has recently learned to speak Bambara/Jula. Abbie did initial fieldwork on Bangime in Bounou June-August 2008, and has returned to the field several times since. Her 2013 PhD dissertation was a description and analysis of aspects of the phonology, morphology, and morphosyntax of Bangime. She has also produced work on Dogon languages' (Kindige, Ibi So) [ATR] systems. She is currently a postdoctoral fellow at SOAS in London, on the Leverhulme funded Crossroads Project focusing on multilingualism among Senegalese languages.""",
        "ahantgan (at) umail.iu.edu",
        "https://soascrossroads.org/team/post-doc-research-fellows/abbie-hantgan/"),
    #(includes a grammar and lexicon of Tiefo, a severely endangered Gur language of SW Burkina Faso)
    #Abbie's article in the Returned Peace Corps Volunteer Newsletter [pdf]

    "Jeffrey Heath": ("""Prof. of Linguistics, University of Michigan (Ann Arbor) is a veteran of more than 14 years of on-location fieldwork. He began with Australian Aboriginal languages of eastern Arnhem Land (1970's), then did various topical projects on Jewish and Muslim dialects of Maghrebi Arabic (1980's). Since 1989 he has made annual trips to Mali where he has worked in succession on Hassaniya Arabic, riverine Songhay languages (Koyra Chiini, Koyraboro Senni), montane Songhay languages (Tondi Songway Kiini, Humburi Senni), and Tamashek (Berber family). Since 2005 he has focused on Dogon languages: Jamsay, Ben Tey, Bankan Tey, Bunoge, Najamba, Nanga, Penange, Tebul Ure, Tiranige, Yanda Dom, Donno So, and Dogul Dom. During his 2011-12 fieldwork stint he has also been shooting and producing low-budget videos of cultural events and everyday practical activities, some of which can be viewed on the project website. He has also been mapping Dogon villages in collaboration with the LLMAP project at Eastern Michigan University, and has continued to work on local flora-fauna and native terms thereof. He is the author of A Grammar of Jamsay (Mouton, 2008), but his more recent Dogon grammars are currently disseminated on the project website or published in the open access digital library Language Description Heritage and permanantly archived at Deep Blue at the University of Michigan. In Burkina, Jeff is working on Tiefo (Gur) in collaboration with others, and on Jalkunan (Mande).""",
        "schweinehaxen (at) hotmail.com",
        "http://www-personal.umich.edu/~jheath/"),

    "Laura McPherson": ("""is an assistant professor in the Linguistics Program at Dartmouth College. Her main theoretical interests are in phonology, tonology, and the phonology-syntax interface. She earned her BA in Linguistics from Scripps College in 2008, working with Africanist Mary Paster on the verbal morphology of Luganda, and her PhD from UCLA in 2014 with the dissertation Replacive grammatical tone in the Dogon languages (co-chairs Bruce Hayes and Russell Schuh). She spent eleven months in Mali on her first field trip (2008-2009) working on Tommo So, first with the support of our project then with the support of a Fulbright Fellowship. She returned to Mali annually to continue work and published A Grammar of Tommo So in the Mouton Grammar Library in 2013. She has more recently shifted focus to Seeku, a Mande language of Burkina Faso and on languages in Melanesia.""",
        "laura.emcpherson (at) gmail.com",
"http://www.dartmouth.edu/~mcpherson/"),

    "Steven Moran": ("""a veteran of the Eastern Michigan University Linguist List and E-MELD team, went on to get a 2012 Ph.D. in Computational Linguistics at the University of Washington with a dissertation title "Phonetics information base and lexicon." He previously did fieldwork in Ghana and published a grammatical sketch of Western Sisaala. He manages the Dogon project website, and has done fieldwork on Toro-So (Sangha So dialect) in 2009 and 2013. He was a postdoc researcher at the University of Munich (Germany) in the project "Quantitative language comparison" funded by the European Research Council from 2012-2014, and is currently a postdoc at the University of Zurich. """,
        "bambooforest (at) gmail.com",
        "http://www.comparativelinguistics.uzh.ch/de/moran.html"),

    "Kirill Prokhorov": ("""is a Russian Ph.D. who has been trained by West African specialists and field-oriented typologists in Moscow and St. Petersburg. Since 2008 he has focused on the Mombo (also known as Kolu-So) language with a base in the picturesque village of Songho just west of Bandiagara. In January 2009 he was a visiting scholar for one month at the Max Planck Institute for Evolutionary Anthropology (MPI-EVA) in Leipzig, which also provided him with a stipend to support his 2008 fieldwork. He has made return trips to Dogon country in 2009, 2010 and 2011. He has also studied Ampari, and did short pilot-studies of Bunoge and Penange. In 2010 was based at Humboldt University (Berlin) where he is working on the project "Predicate-centered focus types: A sample-based typological study in African languages", part of the larger project SFB 632 "Information Structure" funded by German Science Association (DFG).""",
        "bolshoypro (at) gmail.com",
        None),

    "Vu Truong": ("""graduated from Brandeis University with a B.A. in linguistics in 2011. In 2010, he designed and implemented a sociolinguistic survey in Sokone, Senegal on attitudes towards language shift to Wolof. In 2011, he taught English in Kagoshima, Japan as part of the JET Program. He joined the project in August 2012. He was at our base in Bobo Dioulasso from mid-2012 to mid-2014, working on the Jalkunan language (Mande family, about 500 speakers). He is now a student in the Linguistics PhD program at the University of Chicago.""",
        "finath (at) gmail.com",
        None),
    }


class Entry(object):
    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)


def ff_to_standard(d):
    kw = {}
    for k, v in FIELD_MAP.items():
        if v:
            kw[v] = d.get(k)
    return Entry(**kw)


FIELD_MAP = {
    "code (Eng)": "code_eng",
    "subcode (Eng)": "subcode_eng",
    "code (fr)": "code_fr",
    "sous-code (fr)": "sous_code_fr",
    "code #": "code",
    "subcode #": "subcode",
    "order": "subsubcode",
    "short": "short",
    "court": "court",
    "ref#": "ref",
    "jpg": "jpg",
    "video": "video",
    "date": "date",
    "comment": "comment",
    "English": "English",
    "français": "Francais",
    "core": "core",

    "Toro Tegu (Toupere, JH)": "Toro_Tegu",
    "Ben Tey (Beni, JH)": "Ben_Tey",
    "Bankan-Tey (Walo, JH)": "Bankan_Tey",
    "Nanga (Anda, JH)": "Nanga",
    "Jamsay (alphabet)": "Jamsay_Alphabet",
    "Jamsay (Douentza area, JH)": "Jamsay",
    "Perge Tegu (Pergué, JH)": "Perge_Tegu",
    "Gourou (Kiri, JH)": "Gourou",
    "Jamsay (Mondoro, JH)": "Jamsay_Mondoro",
    "Togo-Kan (Koporo-pen, JH with BT)": "Togo_Kan",
    "Yorno-So (Yendouma, JH and DT)": "Yorno_So",
    "Ibi-So (JH)": "",
    "Donno-So": "",
    "Tomo Kan (Segue)": "Tomo_Kan",
    "Tomo Kan (Diangassagou)": "Tomo_Kan_Diangassagou",
    "Tommo So (Tongo Tongo, combined)": "Tommo_So",
    "Tommo So (Tongo Tongo, JH)": "",

    "Tommo-So (Tongo Tongo, LM)": "",
    "Dogul Dom (Bendiely, BC)": "Dogul_Dom",
    "Tebul Ure (JH)": "Tebul_Ure",
    "Yanda Dom (Yanda, JH)": "Yanda_Dom",
    "Najamba (Kubewel-Adia, JH)": "Najamba",
    "Tiranige (Boui, JH)": "Tiranige",
    "Mombo JH": "Mombo",
    "Mombo (Songho, KP)": "",
    "Ampari (Nando, JH)": "Ampari",
    "Ampari (Nando, KP)": "",
    "Bunoge (Boudou)": "Bunoge",
    "Penange (Pinia)": "Penange",

    "Bangime (Bounou, JH)": "",
    "Bangime (Bounou, AH)": "",

    "HS Songhay": "",
    "TSK Songhay": "",
    "species": "species",
    "family": "family",
}
"""
    book p.,
    synonymy,
    comment,
    domain,
    specimen
"""