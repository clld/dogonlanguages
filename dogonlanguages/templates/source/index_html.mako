<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "sources" %>
<%block name="title">${_('Sources')}</%block>

<%def name="contextnav()">
    ${util.contextnavitem('sources', label=_('Sources'))}
    ${util.contextnavitem('files', label='Files')}
</%def>

<h2>${_('Sources')}</h2>

${ctx.render()}
