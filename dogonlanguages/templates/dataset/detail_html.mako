<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
    ${util.cite()}
</%def>

<h2>Dogon and Bangime Linguistics</h2>

<p class="lead">
    This is the website for an NSF-funded fieldwork project on Dogon languages of Mali, also
    including the
    <a href="${request.route_url('bangime')}">Bangime language</a>
    (a language isolate spoken by a culturally Dogon group).
    We also work on
    <a href="${request.route_url('other', _anchor='tiefo')}">Tiefo (two endangered Gur languages of SW Burkina)</a>
    and
    <a href="${request.route_url('other', _anchor='mande')}">Jalkunan (endangered Mande language of SW Burkina)</a>
    and have begun working on
    <a href="${request.route_url('other', _anchor='bozo')}">Bozo-Jenaama (Mali)</a>
    and, in collaboration, on endangered
    <a href="${request.route_url('other', _anchor='mbre')}">Mbre (Bere)</a>
    in Cote d'Ivoire.
</p>
<p>
    We have operated from bases in Douentza and Sevare (near Mopti) in Mali, and (since May 2012)
    in Bobo Dioulasso in neighboring Burkina Faso. We are producing grammar-text-lexicon coverage of
    the individual languages, supplemented by geographical, ethnobiological, and video sub-projects.
    Our early focus was on the northern and eastern Dogon languages and we are gradually moving south and west.
</p>
<p>
    The most theoretically exciting features of Dogon languages are the elaborate tonosyntax especially
    within NP (DP), and the consistent pattern of lexicalizing action verbs with reference to manner/process
    rather than result/function. The most interesting feature of Bangime is its complex system of tonal ablaut,
    both of nouns and verbs.
</p>
<p>
    Nonlinguist viewers will hopefully especially enjoy our
    <a href="${request.route_url('files')}">documentary videos</a>
    and/or our
    <a href="${request.route_url('florafauna')}">flora-fauna materials</a>.
    Enjoy!
</p>
