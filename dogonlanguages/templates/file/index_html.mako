<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "files" %>
<%block name="title">${_('Files')}</%block>

<h2>Files</h2>

<p>
    This page provides a complete list of all media files created within the Dogonlanguages Project.
</p>
<p>
    You may search for certain types of media, e.g. videos, by selecting a suitable
    ${h.external_link('https://en.wikipedia.org/wiki/Media_type', label='media type')}
    from the drop-down list below, e.g. <em>video/quicktime</em> or <em>video/x-msvideo</em>.
</p>
<p>
    You may also exploit the fact that metadata about files is encoded in the file names by
    typing queries into the search box below the <strong>Name</strong> column header, e.g.
    <em>Douentza</em>, to search for all files related to this town.
</p>

${ctx.render()}