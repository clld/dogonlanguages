<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>
<p>${ctx.description}</p>

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#villages" data-toggle="tab">Villages</a></li>
        <li><a href="#lexicon" data-toggle="tab">Lexicon</a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="villages" class="tab-pane active">
            <ul>
            % for village in ctx.villages:
                <li>${h.link(request, village)} ${village.description or ''}</li>
            % endfor
            </ul>
        </div>
        <div id="lexicon" class="tab-pane">
            ${request.get_datatable('values', h.models.Value, language=ctx).render()}
        </div>
    </div>
    <script>
$(document).ready(function() {
    if (location.hash !== '') {
        $('a[href="#' + location.hash.substr(2) + '"]').tab('show');
    }
    return $('a[data-toggle="tab"]').on('shown', function(e) {
        return location.hash = 't' + $(e.target).attr('href').substr(1);
    });
});
    </script>
</div>

<%def name="sidebar()">
    ${util.codes()}
    <div style="clear: right;"> </div>
    <%util:well>
        ${request.map.render()}
        ${h.format_coordinates(ctx)}
    </%util:well>
</%def>
