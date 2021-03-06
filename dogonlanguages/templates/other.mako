# coding: utf8
<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>
<%! active_menu_item = "other" %>
<%block name="title">Other Languages</%block>

<h2>Other Languages</h2>

<p>
In addition to Dogon and Bangime, our NSF-funded project includes Tiefo, Seenku, and Jalkunan in Burkina Faso. We have also hosted and/or supported by University of Michigan or other non-NSF funds, linguists working on Jenaama (Mali), Bobo Maduré and Viemo (Burkina Faso), and Mbre (Côte d'Ivoire). More information on these languages and on what we are doing or hope to do with them, is below
</p>


<%util:section title="Bozo languages of Mali" level="3" id="bozo">
<h4>Jenaama (aka Sorogaama)</h4>

<p>Jenaama is the currently accepted name for a language consisting of multiple dialects, belonging to the Bozo language family, which is part of the larger Mande family. Within Mande, the closest relative of Bozo is thought to be Soninke.</p>

<p>Four Bozo languages are currently recognized:</p>

<table class="table table-nonfluid">
<thead>
<tr>
    <th>Current name</th>
    <th>Synonyms</th>
    <th>ISO code</th>
    <th>Glottolog code</th>
</tr>
</thead>
<tbody>
    % for row in rows:
        <tr>
            % for item in row:
                <td>${item}</td>
            % endfor
        </tr>
    % endfor
</tbody>
</table>

<p>The Bozo (except some Jenaama) are the classic fishing people of the Niger and Bani rivers in Mali. They specialize in hunting fish and either selling them fresh or smoking and drying them for sale throughout the year. Ethnic Bozo fishing people, whether they speak a Bozo language or have been linguistically assimilated (usually to Songhay), are called Sorko.</p>

<p>Jenaama, on the other hand, is spoken not only by Sorko fishers (hence the older language name Sorogaama), but also by rice cultivators in riverine villages and by millet cultivators at the base of the western escarpment (cliffs) of the Dogon plateau and in the sandy plains between the escarpment and the rivers. Jenaama has been subdivided into several "dialects" including Pondori, Kotya, Korondugu, and Debo, though no definite dialectal division has been made. Varieties of Jenaama are spoken in partially separated zones in the vicinities of Djenné, Mopti, Konna, and Lac Débo. Jenaama literally means "Djenné people" but the term is widely used in the farming villages which may be distant from Djenné.</p>

<p>Jeffrey Heath has begun initial fieldwork on the most easterly variety of Jenaama, spoken in and near the villages of Namagué and Kargué. These two villages are located on the slopes of the (low) escarpment of the Dogon plateau, at opposite ends of the mouth of the narrow valley cutting into the plateau where the Bangande (speakers of the Bangime language isolate) have their villages (including Bounou and Bara). Although these Jenaama speakers are immediate neighbors of the Bangande, who pass through the mouth of the valley on their way to weekly markets (Sambere on Sundays, Konna on Thursdays), intermarriage is prohibited and there is very little bilingualism. More generally, Bozo intermarriage with Dogon is prohibited. Bozo and Dogon are traditional "cousins" within the context of inter-ethnic cousinage, a relationship involving separation, symbiosis (Bozo may help resolve intra-Dogon disputes and vice versa), and obligatory ritual joking/insult.</p>

<p>Fulfulde is the lingua franca of the zone and is generally used between Bozo and Dogon, in addition to communication with true Fulbe (cattle herders) and their (ex )slaves, the Rimaibe. There are Fulbe and Rimaibe villages interspersed among Bozo villages in the plains between the rivers and the escarpment. Fulfulde is the primary language of Konna, and of weekly markets in the area.</p>

<p>The Bargué-Namagué variety, which was not included in previous surveys, is referred to by its speakers as the "escarpment" dialect, distinct from the "river" dialect that extends from the rice-fishing villages along the river to the Konna area. In fact, it is not yet clear whether the two varieties are best considered dialects or separate languages.</p>

<p>The cliffs dialect of Jenaama has three tone levels. It also has a few "exotic" phonemes that are absent or uncommon in other languages of the zone:</p>
<ul>
<li>ɥ -- high front rounded semivowel (also found in Bangime)</li>
<li>ɯ -- back unrounded vowel</li>
</ul>

<p>Click on the links below for the current draft of Heath’s Bozo-Jenaama grammar and lexical spreadsheets, representing the state of the art as of early 2019.</p>

<ul>
<li>${h.external_link('https://github.com/clld/dogonlanguages-data/raw/master/beta/literature/Jenaama_Bozo_grammar.docx', label='A Grammar of Jenaama Bozo of Mali, Cliffs variety')}</li>
<li>${h.external_link('https://github.com/clld/dogonlanguages-data/raw/master/beta/literature/JH_Jenaama_lexicon.xlsx', label='Jenaama lexicon')}</li>
</ul>

<p>Heath intends to continue working on Bozo-Jenaama and other Bozo languages as opportunities arise.</p>
</%util:section>


<%util:section title="Gur (?) languages of SW Burkina" level="3" id="tiefo">
<h4>Tiefo languages</h4>
<p>There are two related but mutually unintelligible languages spoken in the Tiefo (cɛ̀fɔ́). One is still spoken by two old people in Nyafogo village; we provisionally call it Tiefo-N. The other is still spoken by one extended multigenerational family in Daramandougou village; we refer to it as Tiefo-D. These labels are short for Tiefo-Nyafogo and Tiefo-Daramandougou, though the term Tiefo-N also includes the recently extinct and largely undocumented dialect of Noumoudara.</p>

<p>Tiefo belongs to a cluster of languages (Viemo, Natioro, Wara, and northern and southern Toussiana) in SW Burkina Faso that have been classified as belonging to the Gur family, but not in any specific division of Gur. The genetic relationship of these languages to each other, and to the core Gur languages, is unclear. The only thing that is clear is that Tiefo-N and Tiefo-D are related.</p>

<p>Neither language has a productive noun-class system. The productive nominal plural in Tiefo-D is by suffixation of -rV where V is a copy of the preceding vowel. In Tiefo-N it is by prolongation of the final vowel or sonorant of the singular. There are also a few irregular plurals that may be vestiges of a class system, as well as synchronically unsegmentable nouns that may contain a frozen class suffix. In verbs, the primary morphological split is between "perfective" and "imperfective" stems, but the two are distributed in a fairly complex way (not governed by strict semantic principles) across phrase-level inflections. The latter include perfective/imperfective, and future crossed with negation for indicatives, and imperative and hortative crossed with negation for deontics.</p>

<p>Tiefo as a whole was thought to be at the verge of extinction, and possibly already extict, by the then leading Gur specialist Gabriel Manessy in the early 1980's: "Le tyefo est selon toute apparence une langue en voie d'extinction, peut-être éteinte aujourd'hui" (1982: 143), The only data available to him was a word-list and a few phrases compiled under difficult conditions by R. P. Prost. Manessy found that of 120 lexical items in the list, 28 could be placed in comparative Gur lexical sets, on the basis of which he classified Tiefo as a genetic outlier within Gur. He made similar remarks about Viemo and other western Gur languages of the zone; see also Naden (1989).</p>

<p>Tiefo-D was studied by Kerstin Winkelmann in her German-language dissertation (1998), based on fieldwork 1990-94. It covers phonology, morphology, and some basics of syntax, and has a mid-sized lexicon as an appendix. In addition to Daramandougou, she also did survey work on Tiefo-N in both Noumoudara and Nyafogo, and included grammar and lexicon notes on them in her work. She observed that Tiefo-N informants, especially in Nyafogo, were semi-speakers who struggled to produce plurals of nouns, and from whom only portions of verb paradigms could be elicited.</p>

<p>In 2012 we discovered that competent informants were still present in Nyafogo, and we began emergency salvage fieldwork. This was initially carried out by Abbie Hantgan. We also found that a Burkinabé linguistics student at the University of Ouagadougou, Aminata Ouattara, was also working on Tiefo-N. She is an ethnic Tiefo but not a native speaker. There were some hitches in the fieldwork due to Hantgan's departure for a post-doc at SOAS in January 2013, and Ouattara's taking a year off to work for an NGO. In 2016 Heath and Ouattara teamed up to do intensive work with the last two fluent Tiefo-N speakers at our base in Bobo Dioulasso with some trips to Nyafogo village. See links below for references. Ouattara defended her master’s thesis on Tiefo-N in early 2019.</p>

<p> In the period 2017-2019 Heath and Ouattara have also done extensive work on Tiefo-D, which is still spoken in some of the quartiers of Daramandougou village cluster. There are four dialects, the most divergent being that of Biton quartier. A grammar and lexical spreadsheets are at an advanced stage as of summer 2019 and will likely be finished in early summer 2020.</p>

<p>A distinctive feature of Tiefo-D grammar is the use of motion verbs 'come' and 'go' in multi-clause constructions. Both verbs occur in constructions of the type 'came and VPed' and 'went and VPed', and elaborations like 'came and came and VPed' and 'went and went and VPed', and even 'came and went and VPed' (not involving round-trip motion), where the motion verbs function to highlight events, with or without involving actual motion. The second motion verb in such constructions is contracted or suppletive.</p>

<p>Funding for the Tiefo-N project was from NSF, and that for the Tiefo-D project is from NEH.</p>

<p>Click on the links for drafts of our own work on Tiefo-N, and English/French adaptations/summaries of Winkelmann's German-language work.</p>

<ul>
<li>${h.external_link('https://doi.org/10.17617/2.2378140', label='Short grammar of Tiefo-N of Nyafogo (Gur, Burkina Faso)')}</li>
<li>${h.external_link('https://deepblue.lib.umich.edu/data/concern/data_sets/x059c7329', label='Lexical documents Tiefo-N language of Burkina Faso')}</li>
<li>${h.external_link('https://github.com/clld/dogonlanguages-data/raw/master/beta/literature/JH_Tiefo_notes_ex_Winkelmann.docx', label='JH_Tiefo_notes_ex_Winkelmann.docx')}</li>
<li>${h.external_link('https://github.com/clld/dogonlanguages-data/raw/master/beta/literature/JH_Tiefo_lexicon_ex_Winkelmann.xlsx', label='JH_Tiefo_lexicon_ex_Winkelmann.xlsx')}</li>
</ul>


<p>References</p>
<ul>
<li>Manessy, Gabriel. 1982. Matériaux linguistiques pour servir à l'histoire des populations du sud-ouest de la Haute-Volta. Sprache und Geschichte in Afrika 4, 95-164.</li>
<li>Naden, Anthony. 1989. Gur. Dans John Bendor-Samuel & Rhonda Hartell (éds.), The Niger-Congo languages: A classification and description of Africa's largest language family, Lanham/New York/London: University Press of America, 140-168.</li>
<li>Winkelmann, Kerstin. 1998. Die Sprache der Cɛfɔ von Daramandugu (Burkina Faso). (Berichte des Sonderforschungsbereichs 268). Frankfurt am Main: Johann Wolfgang Goethe-Universität. ISBN 3-9806129-0-2.</li>
</ul>


<h4>Viemo</h4>
<p>Viemo belongs to a cluster of languages (with Tiefo, Natioro, Wara, and northern and southern Toussiana) in SW Burkina Faso that have been classified as belonging to the Gur family, but not in any specific division of Gur. The genetic relationship of these languages to each other, and to the core Gur languages, is unclear.</p>

<p>Viemo is slowly declining in the face of Jula. It is still spoken by young people, but its lexicon and grammar are undergoing accelerated changes. </p>

<p>Our NSF-funded project hosted (but did not otherwise directly fund) Nathan Severance in our Bobo Dioulasso base in 2014-15 when he was a recent graduate of Dartmouth College; he returned for summer fieldwork 2016, by then as a graduate student in Linguistics at University of Oregon.</p>

<p>Nate's work is on Viemo, and on the sociolinguistics of Viemo and Jula in an increasingly Jula-dominant environment. </p>
</%util:section>


<%util:section title="Mande languages of SW Burkina" level="3" id="mande">
<h4>Bobo Madure</h4>
<p>Bobo Madure is one of approximately four recognized languages of the Bobo subgroup of Mande. They are spoken in and around (mainly north of) Bobo Dioulasso in SW Burkina Faso. Bobo Dioulasso is the second largest city in Burkina. As its name suggests, it has both Bobo and Jula (Dioula) populations, the Bobo being the original inhabitants and the Jula the newcomers.</p>

<p>Our NSF-supported project has also hosted University of Michigan graduate student Kate Sherwood, whose other funding has come from that university. She is a phonologist and phonetician specializing in intonation. She is coming back to Bobo for a long stay beginning September '16, after two previous summer fieldwork stints.</p>

<p>Bobo Madure is not well described in prior literature, so Kate's work includes basic grammatical and tonological analysis of the language, as well as a special focus on terminal intonation patterns.</p>

<h4>Jalkunan</h4>
<p>Jalkunan is a Mande language spoken in the three-part village cluster of Bledougou in the Banfora plateau near the town Sindou. Bledougou is a Mande enclave entirely surrounded by villages speaking Senoufo languages. Until recently, the population of Bledougou was strictly endogamous, but this has been relaxed in recent decades.</p>

<p>The language is declining in vitality, and the best speakers are middle-aged and older. It is therefore a priority for the Burkina wing of our NSF-funded project, which focuses on small-population and endangered languages.</p>

<p>Fieldwork on Jalkunan was carried out by project member Vu Truong in 2013-15, at our base in Bobo Dioulasso with occasional village visits. He was funded for the first year by our project, and in the second year by a Fulbright fellowship. He is now a graduate student at University of Chicago.</p>

<p>With Truong (now Tran Truong) pursuing other interests, Heath took over the Jalkunan project and worked with a speaker in 2016-2017. A grammar (with texts) and lexical spreadsheets came out of this work. </p>

<ul>
<li>${h.external_link('https://doi.org/10.17617/2.2346932', label='A grammar of Jalkunan (Mande, Burkina Faso)')}</li>
<li>${h.external_link('https://deepblue.lib.umich.edu/data/concern/data_sets/gh93gz487', label='Lexical spreadsheets Jalkunan language of Burkina Faso')}</li>
<li>${h.external_link('https://deepblue.lib.umich.edu/data/concern/data_sets/gm80hv964', label='Mande Jalkunan Audio Files')}</li>
</ul>
</%util:section>


<%util:section title="unclassified, Côte d'Ivoire" level="3" id="mbre">
<h4>Pere (also known as Mbre, Bere)</h4>

<p>The Pere language (pronounced pɛ́rɛ́) and previously known in the literature as Mbre, Bere, or Pɛrɛ is spoken in Bonosso village near Tienboué in northern Côte d'Ivoire. Pere is currently thought to be an independent branch of Niger-Congo. Bonosso is surrounded by villages speaking the Koro language, a Manding language related to Bambara and Jula.</p>

<p>Pere was discovered by Deni Creissels who was working on Koro. He called attention to it after he and other Africanists he consulted with could not place it in any recognized language family.</p>

<p>Beginning in 2014 Pere was studied by graduate student Ibrahima Tioté of the University of Cocody in Abidjan. He is a native Koro speaker from a nearby village, so he knows the local environment well. Heath joined with him, initially as a funding source and later as fieldworker. Tioté defended his doctoral dissertation in summer 2018. Heath did final fieldwork in Bonosso in late 2019, and Heath and Tioté did final corrections in early 2019.</p>

<p>Pere linear order is CVOX (perfective) and C-wɔ̀-OVX (imperfective, including an aspect particle meaning 'be'). Negation is clause-final. Suffixal morphology is modest. There is an "absolute" suffix -à on nouns that functions in part like an article, but is not consistently definite. Verbs have tonal ablaut alternations distinguishing perfective from imperfective at the stem level. The most unusual feature of the grammar is the use of three "postposition" look-alikes in phrasal-verb combinations similar to English phrasal verbs (verb plus preposition-like particle).</p>

<ul>
<li>${h.external_link('https://doi.org/10.5281/zenodo.3346581', label="A grammar of Pere (Bere, Mbre) of Côte d'Ivoire")}</li>
<li>${h.external_link('https://doi.org/10.5281/zenodo.3354193', label='Pere lexicon [Data set]')}</li>
<li>${h.external_link('https://doi.org/10.5281/zenodo.3354206', label='Pere lexicon of flora and fauna [Data set]')}</li>
</ul>

</%util:section>

<p>[Jeffrey Heath, last update July 2019]</p>
