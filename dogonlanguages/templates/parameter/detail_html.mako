<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">Concept "${ctx.name}"</%block>
<% images = [f for f in ctx._files if f.mime_type.startswith('image')] %>
<% videos = [f for f in ctx._files if f.mime_type.startswith('video')] %>

% if ctx.family:
    <ul class="breadcrumb">
        % for name in reversed(ctx.family.split(',')):
            <li class="active">${name.strip()}</li> <span class="divider">/</span>
        % endfor
        <li class="active">${ctx.species} ${u.eol_link(request, ctx)}</li>
    </ul>
% endif

<h2>${ctx.name}</h2>

<table class="table table-nonfluid">
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

% if videos:
    <ul class="inline">
    % for vid in videos:
        <li><a href="${u.cdstar_url(vid)}">${u.format_file(vid)}</a></li>
##<video id="video_${vid.pk}" class="video-js vjs-default-skin"
##       controls preload="auto" width="640" height="264"
##       ##poster="http://video-js.zencoder.com/oceans-clip.png"
##       data-setup='{"example_option":true}'>
##    <source src="${u.cdstar_url(vid)}" type='${vid.mime_type}' />
##    <p class="vjs-no-js">To view this video please enable JavaScript, and consider upgrading to a web browser that <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a></p>
##   </video>
    % endfor
    </ul>
% endif

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