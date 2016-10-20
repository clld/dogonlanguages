<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>
<%! active_menu_item = "bangime" %>
<%block name="title">Bangime</%block>

<%def name="contextnav()">
    ${util.contextnavitem('sources', label=_('Sources'))}
    ${util.contextnavitem('typology', label=_('Typology'))}
    ${util.contextnavitem('files', label='Files')}
</%def>

<h2>Typological and historical topics for Dogon</h2>

<p>
    A number of grammatical features that may be of interest to viewers are discussed in the
    informal discussion pieces listed below (click to open). They will give first-time or
    incidental users an initial summary of the most interesting features of these languages.
    Those who wish to follow up can find further details on specific languages in the unpublished
    manuscripts in the bibliography on the materials page, and in published grammars (Jamsay, Tommo So)
    and articles. Some of the pieces include extensive lists of forms, which will help users generate
    ideas about proto-Dogon reconstructions or wider genetic relationships.
</p>

<p>
    Of particular interest to general typology are &quot;syntactic tonology of NP&quot; and
    &quot;relative clauses,&quot; which should be read sequentially, in that order.
</p>

<p>
    The pieces that are up (see below) are written by Jeff Heath and range from the skeletal to the
    relatively comprehensive. They will be updated, and new pieces added, from time to time.
</p>

<p>
    Unlike the rest of this website and the grammar drafts, these discussions contain limited
    exemplification. Please do not cite them as references, rather use them as guides pointing
    to the more authoritative works on specific languages.
</p>

<h3>Phonology</h3>
<table class="table table-nonfluid">
    <tbody>
    ${u.format_document_link(request, docs["dogonatrharmony"], label="Dogon ATR-Harmony")}
    ${u.format_document_link(request, docs["dogonlexicaltonesofverbsandotherstemclasses"], label="Dogon lexical tones of verbs and other stem-classes")}
    ${u.format_document_link(request, docs["dogonvowelsymbolism"], label="Dogon vowel symbolism")}
    ${u.format_document_link(request, docs["dogonnasalizedsonorantsandnasalizationspreading"], label="Dogon nasalized sonorants and Nasalization-Spreading")}
    </tbody>
</table>

<h3>Phonology/syntax</h3>
<table class="table table-nonfluid">
    <tbody>
        ${u.format_document_link(request, docs["dogonsyntactictonologyofnp"], label="Dogon syntactic tonology of NP")}
    </tbody>
</table>

<h3>Morphosyntax</h3>
<table class="table table-nonfluid">
    <tbody>
${u.format_document_link(request, docs["dogonnominalclasses"], label="Dogon nominal classes (human/nonhuman, etc.) and number in NPs")}
${u.format_document_link(request, docs["dogonadpositions"], label="Dogon adpositions")}
${u.format_document_link(request, docs["dogoncasemarking"], label="Dogon case-marking")}
${u.format_document_link(request, docs["dogonreversiveverbs"], label="Dogon reversive verbs")}
${u.format_document_link(request, docs["dogondynamicandstativeverbs"], label="Dogon stative verbs including 'be (somewhere)' and 'have'")}
${u.format_document_link(request, docs["dogonexistentialparticleyv"], label="Dogon Existential particle yv")}
${u.format_document_link(request, docs["dogonmediopassiveandcausative"], label="Dogon Mediopassive and Causative")}
${u.format_document_link(request, docs["dogonidentificationalitisx"], label="Dogon Identificational 'it is X'")}
${u.format_document_link(request, docs["dogonimperativeandhortativeverbs"], label="Dogon imperative and hortative verbs")}
${u.format_document_link(request, docs["dogonfocalization"], label="Dogon focalization")}
${u.format_document_link(request, docs["dogonverbserialization"], label="Dogon verb serialization (chaining)")}
${u.format_document_link(request, docs["dogonrelativeclauses"], label="Dogon relative clauses")}
${u.format_document_link(request, docs["dogondoubleheadedrelativeclauses"], label="Dogon double-headed relative clauses")}
${u.format_document_link(request, docs["dogonlogophorics"], label="Dogon logophorics and other anaphoric pronouns")}
    </tbody>
</table>

<h3>In preparation</h3>
<ul>
<li>Dogon quantifiers ('all', 'each')</li>
<li>Dogon metrically sensitive phonology (syncope/apocope, vowel-height raising)</li>
<li>Dogon reduplication and iteration</li>
<li>Dogon adjectival intensifiers and (other) expressive adverbials</li>
<li>Dogon coordination ('X and Y', 'X or Y')</li>
</ul>
