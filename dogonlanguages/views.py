from clld.db.meta import DBSession
from clld.db.models.common import Source
from clldutils.misc import slug

from dogonlanguages.models import Document


def bangime(req):
    docs = {
        'memorial': 'eldersmemorialcall07',
        'bangerimevocabulaire': 'bangerimevocabulaire',
        'bangerimephrases': 'bangerimephrases',
        'bangerimepres': 'elders2006',
        'blacksmith': 'blacksmithvocabulary',
    }
    return {
        'docs': {k: Source.get(sid) for k, sid in docs.items()}
    }


def florafauna(req):
    note_ids = [
        'fish_notes_Mali_JH',
        'flora_notes_Mali_JH',
        'insect_arthropod_mollusc_notes_Mali_JH',
        'mammal_notes_Mali_JH',
        'reptile_notes_Mali_JH',
        'bird_notes_Mali_JH',
    ]
    return {
        'notes': [Source.get(slug(sid)) for sid in note_ids]
    }


def typology(req):
    docids = [
        "dogonnominalclasses",
        "dogonatrharmony",
        "dogonexistentialparticleyv",
        "dogonidentificationalitisx",
        "dogonmediopassiveandcausative",
        "dogonadpositions",
        "dogoncasemarking",
        "dogondoubleheadedrelativeclauses",
        "dogondynamicandstativeverbs",
        "dogonfocalization",
        "dogonimperativeandhortativeverbs",
        "dogonlexicaltonesofverbsandotherstemclasses",
        "dogonlogophorics",
        "dogonnasalizedsonorantsandnasalizationspreading",
        "dogonrelativeclauses",
        "dogonreversiveverbs",
        "dogonsyntactictonologyofnp",
        "dogonverbserialization",
        "dogonvowelsymbolism",
    ]
    return {'docs': {d.id: d
                     for d in DBSession.query(Document).filter(Document.id.in_(docids))}}


def other(req):
    jenaama = 'Heath2016-Jenaama-lexicon Heath2016-JenaamaBozo'.split()
    rows = [
        ["Tieyaxo", "Tigemaxo", "boz", "tiey1235"],
        ["Tiema Cewe", "Tiema Ce", "boo", "tiem1235"],
        ["Kelenga", "Hainyaxo", "bsx", "hain1253"],
        ["Jenaama", "Sorogaana", "bze", "jena1242"],
    ]
    return {
        'rows': rows,
        'jenaama': [Source.get(slug(sid)) for sid in jenaama]
    }
