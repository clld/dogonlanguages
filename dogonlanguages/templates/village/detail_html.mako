<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "villages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>


<div class="row-fluid" style="margin-top: 10px">
    <div class="span4">
        <h2>${_('Village')} ${ctx.name}</h2>
        <p>${ctx.description}</p>
    </div>
    <div class="span4">
        <dl>
            % if ctx.latitude is not None:
                <dt>Location</dt>
                <dd>
                    ${u.format_coordinates(ctx)}
                </dd>
            % endif
            % if ctx.transcribed_name:
                <dt>Transcribed name</dt>
                <dd>${ctx.transcribed_name}</dd>
            % endif
            % if ctx.languoid:
                <dt>Language</dt>
                <dd>
                    % if ctx.languoid.in_project:
                        ${h.link(request, ctx.languoid)}
                    % else:
                        ${ctx.languoid}
                    % endif
                    % if ctx.jsondata.get('lg comment'):
                        <span class="comment">${ctx.jsondata.get('lg comment')}</span>
                    % endif
                </dd>
            % endif
            % if ctx.surnames:
                <dt>Surnames</dt>
                <dd>${ctx.surnames}</dd>
            % endif
            % if ctx.jsondata.get('industries'):
                <dt>Industries</dt>
                <dd>${ctx.jsondata['industries']}</dd>
            % endif
            % if ctx.jsondata.get('weekly market'):
                <dt>Weekly market</dt>
                <dd>${ctx.jsondata['weekly market']}</dd>
            % endif
        </dl>
    </div>
    % if ctx.latitude is not None:
    <div class="span4 well">
        ${request.map.render()}
    </div>
    % endif
</div>

<% images = [f for f in ctx._files if f.mime_type.startswith('image')] %>

% for files in [images[i:i+3] for i in range(0, len(images), 3)]:
<div class="row-fluid">
    % for file in files:
            <div class="span4 well">
                <div>
                    ${u.linked_image(file)|n}
                </div>
                    <dl>
                        <dt>Description</dt>
                        <dd>${file.description}</dd>
                        % if file.date_created:
                            <dt>Date</dt>
                            <dd>${file.date_created}</dd>
                        % endif
                        <dt>Creator</dt>
                        <dd>
                            <ul class="unstyled">
                                % for ca in file.contributor_assocs:
                                    <li>${h.link(request, ca.contributor)}</li>
                                % endfor
                            </ul>
                        </dd>
                        % if file.latitude:
                            <dt>Location</dt>
                            <dd>${u.format_coordinates(file)}</dd>
                        % endif
                    </dl>
            </div>
    % endfor
</div>
% endfor
