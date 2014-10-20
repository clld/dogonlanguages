<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">Concept "${ctx.name}"</%block>
<% images = [f for f in ctx._files if f.mime_type.startswith('image')] %>
<% videos = [f for f in ctx._files if f.mime_type.startswith('video')] %>

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
            <td>${ctx.subcode.code.name}</td>
            <td>${ctx.subcode.code.description}</td>
        </tr>
        <tr>
            <th>Subdomain</th>
            <td>${ctx.subcode.name}</td>
            <td>${ctx.subcode.description}</td>
        </tr>
    </tbody>
</table>

% if videos:
    % for vid in videos:
<video id="video_${vid.pk}" class="video-js vjs-default-skin"
       controls preload="auto" width="640" height="264"
       ##poster="http://video-js.zencoder.com/oceans-clip.png"
       data-setup='{"example_option":true}'>
    <source src="${request.file_url(vid)}" type='video/mp4' />
    <p class="vjs-no-js">To view this video please enable JavaScript, and consider upgrading to a web browser that <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a></p>
    </video>
    % endfor
% endif

% for chunk in [images[i:i + 3] for i in range(0, len(images), 3)]:
<div class="row-fluid" id="images">
% for f in chunk:
    <div class="span4">
        <div class="well">
            <img src="${request.file_url(f)}" class="image"/>
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