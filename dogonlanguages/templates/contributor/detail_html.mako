<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributors" %>
<%block name="title">Project member ${ctx.name}</%block>

<h2>Project member ${ctx.name}</h2>
<p>${ctx.description}</p>

<h3>Documents</h3>
<ul>
    % for da in ctx.document_assocs:
    <li>${h.link(request, da.document)}: ${da.document.title}</li>
    % endfor
</ul>
