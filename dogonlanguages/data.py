# coding: utf8
from __future__ import unicode_literals, print_function, division


LANGUAGES = {
    'Toro Tegu': (
        'toro1253',
        """("mountain language") is spoken in villages ringing (and formerly on the summits of) Tabi and Sarinyere mountains, southeast and southwest of the large town of Boni. Toro Tegu is unusual in not being strictly verb-final."""
    ),
    'Jamsay': (
        "jams1239",
        """(from a common greeting), the largest-population Dogon language. It is the dominant language of villages in the plains between and northeast of the major inselbergs in the northeastern area. Mainstream Jamsay extends from the Douentza area southeast to Bamba and Koro, and northeast to the Mondoro area (from where some villages extend into Burkina Faso). Mainstream Jamsay is quite uniform."""
    ),
    'Gourou': (
        "guru1265",
        """(ethnic and language name) is spoken in several villages mostly south of Koro."""
    ),
    'Perge Tegu': (
        "perg1234",
        """("Pergue language") is spoken in Pergue village, which is on a rocky shelf near Beni. Pergue also has a dye-ers' quarter where mainstream Jamsay is spoken. There are a few other similar montane villages nearby that are said to have distinctive Jamsay dialects."""
        #Beni-Walo-Nanga subgroup
    ),
    'Bankan Tey': (
        "bank1259",
        """("Walo language"). Spoken in a village cluster Walo (old French spelling Oualo, native name Bankan) at the eastern end of the very long Gandamiya inselberg, not far from Douentza. Walo is a well-known site for pottery-making (large globular water jars without feet). In the past, Walo and Beni had a single chief, alternating between the two villages."""
    ),
    'Ben Tey': (
        "bent1238",
        """("Beni language') is spoken in the villages of Beni and to a lesser extent Gamni (3 km apart). Both villages are on a relatively narrowl rocky shelf (plateau) south of Douentza. A divergent dialect is said to be spoken in the village of Komboy."""
    ),
    'Nanga': (
        "nang1261",
        """(ethnic and language name) is spoken in five primary villages (Anda, Namakoro, Kono, Wakara, and Soroni) in a compact zone about halfway between Douentza and Bandiagara."""
    ),
    #Tommo-Donno subgroup
    'Tommo So': (
        "tomm1242",
        """(variant Tombo So); spoken in a large area in the plateau; said to have four main dialects; large population."""
    ),
    'Donno So': (
        "donn1238",
        """(aka Kamma So) spoken in several villages just east and southeast of Bandiagara."""
    ),
    'Toro So': (
        "toro1252",
        """("mountain language") is the official cover term for a complex of rather divergent varieties (dialects or languages) spoken in the Dogon cultural heartland along and near the cliffs of Bandiagara. Toro So is the basis for the Dogon language (Dogo So) now being taught in schools with government support."""
    ),
    'Yorno So': (
        "yorn1234",
        """(Yendouma village)."""
    ),
    'Youga So': (
        "youg1234",
        """(at least three dialects on or near Youga mountain)."""
    ),
    'Ibi So': (
        "ibis1234",
        """(village of Ibi)."""
    ),
    'Sangha So': (
        "sang1342",
        """(village cluster of Sangha)."""
    ),
    #several varieties in villages on the eastern cliffs (e.g. Ireli).
    #Tengou-Togo group (five varieties usually considered to be dialects of one language)"""
    'Tengu Kan':  (
        "teng1266",
        """is spoken in some villages in the lower cliffs, and extending (perhaps by recent demographic shifts) into the plains around Bankass."""
    ),
    'Togo Kan': (
        "togo1254",
        """is spoken in several villages in the southeastern plains."""
    ),
    'Tenu Kan': (
        "tenu1234",
        """is said to be very close linguistically to Togo Kan (the surname Togo is dominant in both areas). It is spoken in several villages generally south of Togo Kan."""
    ),
    'Gimri Kan':  (
        "guim1240",
        """is spoken in Gimri and some other villages in the southeastern plains near the cliffs."""
    ),
    'Woru Kan':  (
        "woru1234",
        """(or: Wolu Kan) is spoken in several villages extending from the cliffs into the southeastern plains."""
    ),
    'Tomo Kan':  (
        "tomo1243",
        """is a large-population (second only to Jamsay) language spoken in an extensive area in the southern extension of the Bandiagara plateau (e.g. Diangassagou), on the southern cliffs (e.g. Segue), and in the sandy plains east of the cliffs (e.g. Diallassagou)."""
    ),
    # Western
    'Yanda Dom': (
        "yand1257",
        """("Yanda language") is spoken in the Yanda village cluster and in a few additional villages at the base of the cliffs south of Jamsay-speaking Bamba. Former village sites on the high plateau above have been abandoned. The village of Ana has a distinctive dialect.""",
    ),
    'Tebul Ure': (
        "tebu1239",
        """is spoken in another village cluster nearly contiguous to that for Yanda Dom, but mostly on the edge of the high plateau. Yanda Dom and Tebul Ure are geographically separated from other western Dogon languages.""",
    ),
    'Najamba-Kindige': (
        "bond1248",
        """(exonym Bondu So) is thought to be a single language with much dialectal diversity, but Kindige has not yet been studied in depth. Najamba is the local name for the language in several villages in a large canyon beginning just east of Douentza and ending at the huge central Dogon plateau (e.g. Kubewel, Adia). Kindige is an informal local name for the dialects spoken along the highway running west from Douentza (separated from Najamba by a long inselberg and then by the plateau) and into the high plateau including the Borko area.""",
    ),
    'Dogul Dom': (
        "dogu1235",
        """(or Dogulu) is spoken over a wide but sparsely-populated area on the high, flat plateau that begins a few kilometers north of Bandiagara and south of the Tommo So zone.""",
    ),
    'Tiranige Diga': (
        "tira1258",
        """(or just Tiranige, exonym Duleri) is spoken in a fairly wide area including villages on the northwestern edge of the high plateau and in the plains just below (e.g. Boui). Its genetic position vis-a-vis the Mombo-Ampari group is not yet understood.""",
    ),
    'Mombo': (
        "momb1254",
        """(exonym Kolu So) is spoken in several villages including Songho that are on or near the highway from Mopti-Sevare to Bandiagara. The Nyambeenge and Ambaleenge varieties reported on Blench's website as potentially distinct languages may turn out to be dialects of Mombo from a linguist's perspective, though not necessarily from that of the local people. Most of our data are from Songho village; other dialects like that of Ficko are said to be quite different.""",
    ),
    'Ampari': (
        "ampa1238",
        """is spoken in a smaller area south of the Mombo area, including Nando village.""",
    ),
    'Penange': (
        "pena1270",
        """is closely related to Ampari. It is spoken in the rather isolated village of Pinia, which is located on a rocky hill with a deep rock pond.""",
    ),
    'Bunoge': (
        "buno1241",
        """(exonyms include Korandabo) is spoken in the villages of Boudou and Sangou. It is a small-population language and potentially endangered.""",
    ),

    'Bangime': (
        'bang1363',
        """(=Bangeri Me) is an apparent language isolate with no demonstrated genetic relatives. It is of great potential interest to African linguistics as a possible pre-Niger-Congo remnant similar to Basque in Europe. Alternatively, it could represent a population displacement from farther east in Africa. It is spoken in a small cluster of villages (the largest being Bounou) that are located in a canyon in the inselbergs northeast of Mopti-Sevare. The nearest market towns on the highway from Mopti to Gao are the villages of Sambere (market on Sunday) and Kona (market on Thursday)."""
    )
}

GPS_LANGS = {
    "Ampari": "ampa1238",
    "Bangime": "bang1363",
    "Bankan Tey": "bank1259",
    "Ben Tey": "bent1238",
    "Bomu": "bomu1247",
    "Bozo": "bozo1252",
    "Bunoge": "buno1241",
    "Dogul Dom": "dogu1235",
    "Donno So": "donn1238",
    "Fulfulde": "west2454",
    "Humburi Senni": "humb1243",
    "Jamsay": "jams1239",
    "Koyraboro Senni": "koyr1242",
    "Manding": "mand1435",
    "Mombo": "momb1254",
    "Moore (Mossi)": "moss1236",
    "Najamba-Kindige": "bond1248",
    "Nanga": "nang1261",
    "Penange": "pena1270",
    "Tamashek": "tama1365",
    "Tebul Ure": "tebu1239",
    "Tengou Kan": "",
    "Tiranige": "tira1258",
    "Togo Kan": "togo1254",
    "Tommo So": "tomm1242",
    "Tommo So? Tengou Kan?": None,
    "Tomo Kan": "tomo1243",
    "Tondi Songway Kiini": "tond1249",
    "Toro So": "toro1252",
    "Toro Tegu": "toro1253",
    "Western Songhay": "nort2822",
    "Yanda Dom": "yand1257",
}

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
    "species": "species",
    "family": "family",
}

LEX_LANGS = {
    'flora_Dogon_Unicode': {
        "Toro Tegu (Toupere, JH)": "toro1253",
        "Ben Tey (Beni, JH)": "bent1238",
        "Bankan-Tey (Walo, JH)": "bank1259",
        "Nanga (Anda, JH)": "nang1261",
        "Jamsay (Douentza area, JH)": "jams1239",
        "Perge Tegu (Pergué, JH)": "perg1234",
        "Gourou (Kiri, JH)": "guru1265",
        "Togo-Kan (Koporo-pen, JH with BT)": "togo1254",
        "Yorno-So (Yendouma, JH and DT)": "yorn1234",
        "Ibi-So (JH)": "ibis1234",
        "Donno-So (JH)": "donn1238",
        "Tomo Kan (Segue)": "tomo1243",
        #"Tomo Kan (Diangassagou)": "",
        "Tommo So (Tongo Tongo, JH)": "tomm1242",
        #"Tommo-So (Tongo Tongo, LM)": "",
        "Dogul Dom (Bendiely, BC)": "dogu1235",
        "Tebul Ure (JH)": "tebu1239",
        "Yanda Dom (Yanda, JH)": "yand1257",
        "Najamba (Kubewel-Adia, JH)": "bond1248",
        "Tiranige (Boui, JH)": "tira1258",
        "Mombo JH": "momb1254",
        #"Mombo (Songho, KP)": "",
        "Ampari (Nando, JH)": "ampa1238",
        #"Ampari (Nando, KP)": "",
        "Bunoge (Boudou)": "buno1241",
        "Penange (Pinia)": "pena1270",
        "Bangime (Bounou, SE/JH)": "bang1363",
    },
    'fauna_Dogon_Unicode': {
        "Toro Tegu (Toupere, JH)": "toro1253",
        "Ben Tey (Beni, JH)": "bent1238",
        "Bankan-Tey (Walo, JH)": "bank1259",
        "Nanga (Anda, JH)": "nang1261",
        "Jamsay (Douentza area, JH)": "jams1239",
        "Perge Tegu (Pergué, JH)": "perg1234",
        "Gourou (Kiri, JH)": "guru1265",
        "Togo-Kan (Koporo-pen, JH with BT)": "togo1254",
        "Yorno-So (Yendouma, JH and DT)": "yorn1234",
        "Ibi-So (JH)": "ibis1234",
        "Donno-So": "donn1238",
        "Tomo Kan (Segue)": "tomo1243",
        #"Tomo Kan (Diangassagou)": "",
        "Tommo So (Tongo Tongo, combined)": "tomm1242",
        #"Tommo So (Tongo Tongo, JH)": "",
        #"Tommo-So (Tongo Tongo, LM)": "",
        "Dogul Dom (Bendiely, BC)": "dogu1235",
        "Tebul Ure (JH)": "tebu1239",
        "Yanda Dom (Yanda, JH)": "yand1257",
        "Najamba (Kubewel-Adia, JH)": "bond1248",
        "Tiranige (Boui, JH)": "tira1258",
        "Mombo JH": "momb1254",
        #"Mombo (Songho, KP)": "",
        "Ampari (Nando, JH)": "ampa1238",
        #"Ampari (Nando, KP)": "",
        "Bunoge (Boudou)": "buno1241",
        "Penange (Pinia)": "pena1270",
        "Bangime (Bounou, JH)": "bang1363",
        #"Bangime (Bounou, AH)": "",
    },
    'dogon_lexicon': {
        "Yorno-So": "yorn1234",
        "Toro Tegu (Tabi, JH)": "toro1253",
        "Ben Tey (Beni, JH)": "bent1238",
        "Yanda Dom (Yanda, JH)": "yand1257",
        "Jamsay (Douentza, JH)": "jams1239",
        "Perge Tegu (Pergué, JH)": "perg1234",
        "Gourou (Kiri, JH)": "guru1265",
        "Nanga (Anda, JH)": "nang1261",
        "Bankan-Tey (Walo, JH)": "bank1259",
        "Najamba (Kubewel-Adia, JH)": "bond1248",
        "Tommo-So (Tongo Tongo, LM)": "tomm1242",
        "Togo-Kan (Koporo-pen, JH with BT)": "togo1254",
        "Mombo (Songho, KP)": "momb1254",
    },
}

for k, v in LEX_LANGS.items():
    assert len(set(v.values())) == len(v)
    for gc in v.values():
        if gc not in [r[0] for r in LANGUAGES.values()]:
            raise ValueError(gc)  # pragma: no cover

MOVIES = [
    (
        'Festivals, events, and music',
        'Bamba fishfest 2010',
        'Bamba',
        'Bamba_fishfest_2010',
    ),
    (
        'Festivals, events, and music',
        'Coronation at Hombori 2011',
        'Hombori [Songhay]',
        'Coronation_at_Hombori_2011',
    ),
    (
        'Festivals, events, and music',
        'Cowfest at Bamguel 2011',
        'Bamguel [Fulbe]',
        'cowfest_at_Bamguel_2011',
    ),
    (
        'Festivals, events, and music',
        'Degeju festival at Yendouma 2012',
        'Yendouma',
        'Degeju_festival_Yendouma_2012',
    ),
    (
        'Festivals, events, and music',
        'Dogon cowfest at Pergue 2011',
        'Pergue',
        'Dogon_cowfest_at_Pergue_2011',
    ),
    (
        'Festivals, events, and music',
        'Ginna Dogon 2011 Bandiagara',
        'Bandiagara',
        'Ginna_Dogon_2011_Bandiagara_med_res',
    ),
    (
        'Festivals, events, and music',
        'Koira Bery Festival 2010',
        'Koira Bery',
        'Koira_Bery_festival_2010',
    ),
    (
        'Festivals, events, and music',
        'Songho circumcision 2010',
        'Songho',
        'Songho_circumcision_2010',
    ),
    (
        'Festivals, events, and music',
        'Tabaski at Bounou',
        'Bounou',
        'Tabaski_at_Bounou_2011',
    ),
    (
        'Festivals, events, and music',
        'Tomtoms of Tupere',
        'Toupere',
        'Tomtoms_of_Tupere',
    ),
    (
        'Festivals, events, and music',
        'Yanda huntfest 2010',
        'Yanda',
        'Yanda_huntfest_2010',
    ),
    (
        'Food and drink preparation',
        'Arakam, shepherds bread',
        'Beni',
        'arakam_shepherds_bread_Beni_2011',
    ),
    (
        'Food and drink preparation',
        'Beer brewing',
        'Yanda',
        'beer_brewing_Yanda_2011',
    ),
    (
        'Food and drink preparation',
        'Cooked spiced millet with roselle leaves',
        'Oualo (lower)',
        'cooked_spiced_millet_with_roselle_leaf_Walo_2011',
    ),
    (
        'Food and drink preparation',
        'Cream of millet with curdled milk',
        'Beni',
        'cream_of_millet_with_curdled_milk_Beni_09_2011',
    ),
    (
        'Food and drink preparation',
        'Cream of millet with tamarind',
        'Bendiely',
        'cream_of_millet_with_tamarind_Bendiely_2011',
    ),
    (
        'Food and drink preparation',
        'Daaraa, cooked spiced ground millet with butter',
        'Beni',
        'daaraa_cooked_spiced_ground_millet_with_butter_Beni_2011',
    ),
    (
        'Food and drink preparation',
        'Nuwipara, Cowpea and millet meal',
        'Beni',
        'nuwiiparaa_cowpea_and_millet_meal_Beni_2011',
    ),
    (
        'Food and drink preparation',
        'Flavored cream of millet',
        'Beni',
        'flavored_cream_of_millet_Beni_09_2011',
    ),
    (
        'Food and drink preparation',
        'Pirikesere, simple cooked ground millet',
        'Beni',
        'pirikesere_simple_cooked_ground_millet_Beni_2011',
    ),
    (
        'Food and drink preparation',
        'Roasting half-ripe millet',
        'Beni',
        'roasting_halfripe_millet_Beni_2011',
    ),
    (
        'Food and drink preparation',
        'Sagusooro, cooked millet with roselle leaf sauce',
        'Beni',
        'sarabuguru_cooked_ground_millet_with_roselle_sauce',
    ),
    (
        'Food and drink preparation',
        'Spiced millet rolls',
        'Beni',
        'spiced_millet_rolls_piramang_Beni_2011',
    ),
    (
        'Food and drink preparation',
        'Steamed cowpea leaves with millet',
        'Oualo (lower)',
        'steamed_cowpeas_with_millet_Walo_2011',
    ),
    (
        'Agriculture',
        'Cowpea farming',
        'Sevare',
        'cowpea_farming_Sevare_2011',
    ),
    (
        'Agriculture',
        'Driving off grain-eating birds',
        'Beni',
        'driving_off_grain_eating_birds_Beni_2011',
    ),
    (
        'Agriculture',
        'Fonio farming',
        'Bendiely',
        'fonio_farming_Bendiely_2012',
    ),
    (
        'Agriculture',
        'Groundnut farming',
        'Beni',
        'groundnut_farming_Beni_2011',
    ),
    (
        'Agriculture',
        'Millet farming on the plains',
        'Sevare',
        'millet_farming_plains',
    ),
    (
        'Agriculture',
        'Peanut_farming',
        'Sevare',
        'peanut_farming_Dogon',
    ),
    (
        'Agriculture',
        'Roselle farming',
        'Bendiely & Sevare',
        'roselle_farming_Bendiely_Sevare_Beni',
    ),
    (
        'Agriculture',
        'Rice harvest and threshing',
        'Bounou',
        'rice_harvest_and_threshing_Bounou_2011',
    ),
    (
        'Agriculture',
        'Sesame farming',
        'Beni',
        'sesame_farming_Beni_2011',
    ),
    (
        'Herding and dairy',
        'Curdled milk',
        'Nokara [Fulbe]',
        'curdled_milk_Nokara_2011',
    ),
    (
        'Herding and dairy',
        'Milking cows Fulbe style',
        'Nokara [Fulbe]',
        'milking_cows_Fulbe_2011',
    ),
    (
        'Hunting and collecting',
        'Caterpillars form the shea butter tree',
        'Bobo',
        'ChenillesdeKarite',
    ),
    (
        'Hunting and collecting',
        'Collecting honey',
        'Beni',
        'Collecting_honey_Beni_2011',
    ),
    (
        'Hunting and collecting',
        'Grasshopper hunt',
        'Beni',
        'grasshopper_hunt_Beni_2011',
    ),
    (
        'Hunting and collecting',
        'Water lily harvest',
        'Beni',
        'water_lily_harvest_Beni_2011',
    ),
    (
        'Hunting and collecting',
        'Wild fonio (Panicum laetum)',
        'Toupere',
        'wild_fonio_Panicum_laetum_Tupere_2011',
    ),
    (
        'Oils, soda ash, and soap',
        'Cottonseed oil compilation',
        'Douentza',
        'cottonseed_oil_Douentza_2010',
    ),
    (
        'Oils, soda ash, and soap',
        'Liquid soda ash',
        'Douentza',
        'liquid_soda_ash_Douentza_2010',
    ),
    (
        'Oils, soda ash, and soap',
        'Making soap',
        'Beni',
        'soap_Beni_2011',
    ),
    (
        'Oils, soda ash, and soap',
        'Peanut oil compilation',
        'Douentza',
        'peanut_oil_Douentza_2010',
    ),
    (
        'Oils, soda ash, and soap',
        'Sesame oil compilation',
        'Douentza',
        'sesame_oil_Douentza_2010',
    ),
    (
        'Oils, soda ash, and soap',
        'Shea butter compilation',
        'Douentza',
        'shea_butter_Douentza_2010',
    ),
    (
        'Oils, soda ash, and soap',
        'Wild date oil compilation',
        'Douentza',
        'wild_date_oil_Douentza_2010',
    ),
    (
        'Oils, soda ash, and soap',
        'Wild grape seed oil',
        'Beni',
        'wild_grape_seed_oil_Beni_2011',
    ),
    (
        'Oils, soda ash, and soap',
        'Wild grape seed oil compilation',
        'Douentza',
        'wild_grape_seed_oil_compilation_Douentza_2010',
    ),
    (
        'Spinning, weaving, dye-ing, tailoring',
        'Cotton ginning and spinning compilation',
        'Douentza',
        'Cotton_ginning_spinning_compilation',
    ),
    (
        'Spinning, weaving, dye-ing, tailoring',
        'Weaving',
        'Beni',
        'weaving_Beni_2011',
    ),
    (
        'Tanning and leatherwork',
        'Making a goatskin shoulderbag compilation',
        'Douentza',
        'making_a_goatskin_shoulderbag_compilation_Douentza_2010',
    ),
    (
        'Tanning and leatherwork',
        'Tanning a goat hide compilation',
        'Douentza',
        'tanning_a_goat_hide_Douentza_2010',
    ),
    (
        'Construction, home repair, and carpentry',
        'Replastering a wall',
        'Sevare',
        'replastering_Sevare',
    ),
    (
        'Pottery',
        'Pottery making at Walo',
        'Oualo (lower)',
        'pottery_making_Walo_2010',
    ),
    (
        'Grooming',
        'Hombori yolo coiffure',
        'Hombori',
        'Hombori_yolo_coiffure',
    ),
]
