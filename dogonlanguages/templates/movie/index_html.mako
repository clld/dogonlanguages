<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "movies" %>
<%block name="title">Documentary videos</%block>

<h2>Documentary videos</h2>

<p>
    This page presents videos that we have made. They are mostly of Dogon but include some
    Fulbe, Songhay, and other material which may eventually be migrated to other websites.
    The movies can be viewed online or downloaded.
</p>

<p>
    There is a distinguished tradition of ethnographic film on Dogon. The early films of
    Jean Rouch on the Sigui ritual and on Dogon mortuary customs are classics. The 4 DVD
    compilation &quot;Jean Rouch, une aventure africaine&quot; is available at
    ${h.external_link('http://www.editionsmontparnasse.fr/', label='http://www.editionsmontparnasse.fr')}.
    The magnificant 1997 documentary Inagina by Swiss archeologist Eric Huysecom and cameraman
    Bernard Augustoni re-enacts the by then nearly lost art of iron smelting in the Tomo Kan speaking
    zone: ${h.external_link('http://www.der.org/films/inagina.html', label='http://www.der.org/films/inagina.html')}.
</p>

<p>
    Our &quot;movies&quot; include a few early ones, with &quot;compilation&quot; included in the title, that are
    simply stitched-together sequences of short lexical clips that are parts of complex activities
    (e.g. Ginning and Spinning Cotton, Shoulderbag). The other &quot;movies&quot; are mini-documentaries
    ranging from 1 to 24 minutes, with English subtitles. In some movies that depict complex activities,
    native terms for things and actions have been embedded in the subtitles; see e.g. Weaving.
</p>

<p>
    Camera credits are given in each movie. Project assistant Minkailou Djiguiba shot several of them
    (e.g. Collecting Honey, Degeju festival at Yendouma 2012, and Beer brewing). Ibrahima Cisse shot
    the two Fulbe milk-related movies. Abdoulsalam Maiga and Boubacar Maiga shot all or part of the
    Hombori Songhay movies. Editing and titling has been done by Jeff Heath, who also shot the footage
    for several movies. For &quot;Ginna Dogon 2011 Bandiagara&quot;, the QuickTime version is original and the
    converted AVI copy may be of lower quality. In most other cases the AVI version is at least as good
    as the QuickTime version and may be better and/or more up to date. Recent movies have been made with an AVS
    video.
</p>

<p>
    The movies as presented here are works in progress and will be tweaked. We will reshoot or add scenes
    as opportunities are presented. Further editing of existing scenes will involve color/lighting correction,
    cropping (to reconcile 4:3 and widescreen formats within each movie), and audio improvement. We will also
    add native-language vocabulary embeds in some movies that currently lack them.
</p>

<p>
    We have screened many of the current versions of the movies in Dogon villages, typically outdoors
    in the evening with a laptop set up on a chair. These screenings have attracted large and enthusiastic
    crowds, and we now see dissemination of the movies as a high priority. Eventually we (or anyone else)
    can overdub them in French and in various native languages and offer DVD copies to teachers and local intellectuals.
</p>

<p>
    Note that many of these videos are rather large files. For best results, you may want to &quot;right-click&quot; the
    link and &quot;save-link-as&quot; to save the file to your local computer.
</p>

${ctx.render()}