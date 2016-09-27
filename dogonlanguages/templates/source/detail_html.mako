<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "sources" %>
<%block name="title">${ctx.name}</%block>
<% bibrec = ctx.bibtex() %>

<h2>${ctx.name}</h2>
${ctx.coins(request)|n}

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#tab1" data-toggle="tab">Text</a></li>
        <li><a href="#tab2" data-toggle="tab">BibTeX</a></li>
        <li><a href="#tab3" data-toggle="tab">RIS</a></li>
        <li><a href="#tab4" data-toggle="tab">MODS</a></li>
    </ul>
    <div class="tab-content">
        <div id="tab1" class="tab-pane active">
            <p id="${h.format_gbs_identifier(ctx)}">${bibrec.text()|n}</p>

            % if ctx.datadict().get('Additional_information'):
            <p>
                ${ctx.datadict().get('Additional_information')}
            </p>
            % endif
            % if ctx.url and not ctx.project_doc:
                <p>${h.external_link(ctx.url)}</p>
            % endif
            ${util.gbs_links(filter(None, [ctx.gbs_identifier]))}
            % if ctx.jsondata.get('internetarchive_id'):
                <hr />
                <iframe src='https://archive.org/stream/${ctx.jsondata['internetarchive_id']}?ui=embed#mode/1up' width='680px' height='750px' frameborder='1' ></iframe>
            % endif
        </div>
        <div id="tab2" class="tab-pane"><pre>${bibrec}</pre></div>
        <div id="tab3" class="tab-pane"><pre>${bibrec.format('ris')}</pre></div>
        <div id="tab4" class="tab-pane"><pre>${bibrec.format('mods')}</pre></div>
    </div>
</div>

<%def name="sidebar()">
% if ctx.project_doc:
    <%util:well title="DLP Document">
        % if ctx.contributors:
            <ul class="unstyled">
                % for c in ctx.contributors:
                    <li>${h.link(request, c)}</li>
                % endfor
            </ul>
        % endif
        % if ctx._files:
            <ul class="unstyled">
                % for c in ctx._files:
                    <li><a href="${u.cdstar_url(c)}">${u.format_file(c)}</a></li>
                % endfor
            </ul>
        % endif
    </%util:well>
% endif
</%def>
