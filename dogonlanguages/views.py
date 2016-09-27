from __future__ import unicode_literals

from clld.db.models.common import Source
from clldutils.misc import slug


def bangime(req):
    docs = {
        'memorial': 'eldersmemorialcall07x1',
        'bangerimevocabulaire': 'bangerimevocabulairex1',
        'bangerimephrases': 'bangerimephrasesx1',
        'bangerimepres': 'elders2006x1',
        'blacksmith': 'blacksmithvocabularyx1',
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
        'notes': [Source.get(slug(sid) + 'x1') for sid in note_ids]
    }
