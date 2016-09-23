<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Languages')}</%block>

<h2>${_('Languages')}</h2>
<p>
    The inventory below of Dogon languages is based partially on our own work and partially
    on the literature, primarily the SIL survey and the survey work by Roger Blench
    (see links at end). Bangime is not a Dogon language genetically, and at least in the 4
    West African context it is a language isolate. See also the "typology" page on this
    website for typological profiles.
</p>
<p>
    There is some evidence for a binary genetic split between eastern Dogon and western
    Dogon subgroups. Some genetically "western" languages (Yanda Dom, Tebul Ure) are now
    spoken rather far to the east because of migrations. Some outlier languages such as
    Toro Tegu (far north) and Tomo Kan (far south) fit uneasily into these binary categories.
</p>
<p>
    Where possible we base the names of languages and dialects on endonyms (the names given
    by speakers to their own language, in their own language) rather than on exonyms (language
    and sub-ethnicity names used by others, including other Dogon). However, many "languages"
    (as understood by linguists) are unnamed, as Dogon in many areas (especially Toro So,
    Tengou-Togo, and Najamba-Kindige) use more precise labels denoting what linguists consider
    to be "dialects." For example, "Najamba-Kindige" is our concatenation of Najamba and Kindige,
    which denote two distinct speech varieties (and sub-ethnicities), while "Bondu" is the
    exonym used by other Dogon and Fulbe. Other exonyms include "Kolu" corresponding to our
    "Mombo," and "Duleri" corresponding to our "Tiranige."
</p>
<p>
    Several of the terms in common use in the literature are compounds ending in Kan, So, Dom,
    or Tegu. These are nouns meaning 'speech, language'. Where the compound initial is the
    name of a village (e.g. Beni, Pergue, Ibi), a zone (e.g. Toro 'mountain'), or of a
    surname (Togo), the compound final is useful. Where the compound initial is an ethnic name
    or a high-visibility greeting (Jamsay), the final is unnecessary; compare the fluctuation
    between "Indonesian" and "Bahasa Indonesia" as a language name.
</p>

${request.map.render()}

${ctx.render()}


