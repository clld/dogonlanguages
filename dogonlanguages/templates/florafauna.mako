<%inherit file="${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="util.mako"/>
<%! active_menu_item = "florafauna" %>
<%block name="title">Flora and Fauna</%block>

<h2>Flora and Fauna</h2>
<p>
On this page we present lexical data relating to flora and fauna, and
identification guides to species especially of the Dogon region.
</p>

<p>
We have worked hard to collect (or photograph) flora and fauna specimens and connect biological
taxa to native terms. The work is ongoing, and as of 2012 our data are least complete and reliable
for the more southerly Dogon languages such as Tomo Kan, Donno So, and Toro So.
</p>

<p>
We have worked with several zoologists and botanists, mostly based in Europe, on the identification
of natural species. We gratefully acknowledge the assistance of German herpetologists Wolfgang Boehme
and Ulrich Joger (reptiles and frogs), botanists Pierre Poilecot (deceased 2012) and Michel Arbonnier
of CIRAD-Montpellier, and entomologist Henri-Pierre Aberlenc also of CIRAD-Montpellier. Thanks to
them and to the increasing number of published guides to West African species, we are now able to
identify most new specimens ourselves.
Environment
</p>

<p>
Dogon inhabit an essentially continuous geographical block whose major topographic divisions are the
plateau (high and low), sandy plains (either flat or with dune ridges), and the cliffs that lead down
from the plateau to the plains. There are no major rivers, but there are many seasonal rivers
(rainy season June to September and a few months thereafter) and some year-round ponds and springs.
Viewers can get a sense of the various environments by looking at
the <a href="${request.route_url('villages')}">images and videos of individual villages</a>.
</p>

<h3>Identification guides to flora and fauna</h3>

<p>
These informal guides to flora and fauna of central and northern Mali, focused for now on Dogon country
but including information relevant to northern Mali (Songhay, Fulbe, Arab, and Tamashek speaking zones),
are compiled from the literature and from our own accumulated knowledge. No project member is a
professional biologist. We plan to expand these guides by incorporating ethnobiological information.
Send comments and corrections to Jeffrey Heath at this address: schweinehaxen (at) hotmail.com.
</p>
<ul>
    % for s in notes:
    <li>${h.link(request, s, label=s.title)}</li>
    % endfor
</ul>

## Click links to the various online guides (they may be slow to load):

<h3>Native names for flora-fauna taxa</h3>

<p>
Flora and fauna terms in Dogon languages, as well as Bangime and montane Songhay (Humburi Senni, Tondi
Songway Kiini), are presented in these downloadable spreadsheets (.xls format). Each taxon has a
five-digit reference number (leftmost column) that can be used to search for images.
</p>

${request.get_datatable('values', h.models.Value, ff=True).render()}

