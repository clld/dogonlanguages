<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">Concept "${ctx.name}"</%block>
<% images = [f for f in ctx._files if f.mime_type.startswith('image')] %>
<% videos = [f for f in ctx._files if f.mime_type.startswith('video')] %>

% if ctx.family or ctx.species:
    <ul class="breadcrumb">
        % if ctx.family:
            % for name in reversed(ctx.family.split(',')):
                <li class="active">${name.strip()}</li> <span class="divider">/</span>
            % endfor
        % endif
        % if ctx.species:
            <li class="active">${ctx.species}</li>
        % endif
    </ul>
% endif

<ul class="inline codes pull-right">
    % if ctx.tsammalex_taxon:
        <li>
            <a href="${ctx.tsammalex_url}">
                <span class="large label label-info">
                    Tsammalex: ${ctx.tsammalex_taxon}
                </span>
            </a>
        </li>
    % endif
    % if ctx.eol_url:
        <li>
            <a href="${ctx.eol_url}">
                <span class="large label label-info">EOL</span>
            </a>
        </li>
    % endif
    % if ctx.concepticon_id:
        <li>
            <a href="${ctx.concepticon_url}">
                <span class="large label label-info">
                    Concepticon: ${ctx.concepticon_id}
                </span>
            </a>
        </li>
    % endif
</ul>

<div class="row-fluid" style="margin-top: 10px">
    <div class="span8">
        <h2>${ctx.name}</h2>
<table class="table">
    <thead>
        <tr>
            <th></th>
            <th>English</th>
            <th>French</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>Gloss</th>
            <td>${ctx.name}</td>
            <td>${ctx.description}</td>
        </tr>
        <tr>
            <th>Domain</th>
            <td>${ctx.subdomain.domain.name}</td>
            <td>${ctx.subdomain.domain.description}</td>
        </tr>
        <tr>
            <th>Subdomain</th>
            <td>${ctx.subdomain.name}</td>
            <td>${ctx.subdomain.description}</td>
        </tr>
    </tbody>
</table>
</div>
    <div class="span4">
        % if videos:
            <div class="well">
                ${u.video_detail(*videos)|n}
            </div>
        % endif
    </div>
</div>


% for chunk in [images[i:i + 3] for i in range(0, len(images), 3)]:
<div class="row-fluid" id="images">
% for f in chunk:
    <div class="span4">
        <div class="well">
            ${u.linked_image(f)|n}
        </div>
    </div>
% endfor
</div>
<hr/>
% endfor

% if map_ or request.map:
${(map_ or request.map).render()}
% endif

${request.get_datatable('values', h.models.Value, parameter=ctx).render()}