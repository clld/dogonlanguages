<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<h2>Lexicon</h2>
<p>
    This page provides resources (downloadable spreadsheets and web-based resources) relating to lexicon.
</p>
<p>
    Of particular theoretical interest is our finding that contextually unmarked Dogon action verbs are
    consistently lexicalized with specific reference to manner/process, versus a result/function-based
    lexicalization pattern for English. This applies across a wide range of action-verb categories.
    See ${h.link(request, heathmcpherson2009actionverbs)}.
</p>
<p>
    For project-internal purposes, our comparative Dogon lexical data are organized in an Excel spreadsheet
    with a column for each linguistic variety, and columns for full English and French glosses,
    short English and French glosses (used as finder lists), semantic domain and subdomain (in English, French, and numerical codes),
    sequential order from "1" up within a subdomain (to facilitate elicitation), a five-digit reference number
    that remains stable when an item is modified or relocated, and time of creation ("old" for the oldest entries,
    later ones by year). The existence of a video and/or an image is indicated in other columns. The items are
    also ranked by priority, with "1" for the most basic items. Readers may download the
    ${h.link(request, spreadsheets[0], label=spreadsheets[0].title)}
    instead of or in addition to using the web-based tools below.
    A stripped-down lexical template, minus the Dogon language data, can be used in new fieldwork and might be
    adaptable to non-Dogon languages.
</p>
<h3>Lexical data in spreadsheets</h3>
<ul>
    % for sheet in spreadsheets:
        <li>
            ${h.link(request, sheet, label=sheet.title)}
        </li>
    % endfor
</ul>
<div>
    ${ctx.render()}
</div>
