<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Village')} ${ctx.name}</h2>
<p>${ctx.description}</p>

    % for file in ctx._files:
        % if file.mime_type.startswith('image'):
            <div class="span9">
                <div class="well">
                    ##<a href="${f.jsondata.get('url')}" title="view image">
                        ##<img src="${f.jsondata.get('web')}" class="image"/>
                    ##</a>
                    <img src="${h.data_uri(request.file_ospath(file), file.mime_type)}" class="image">
                </div>
            </div>
            <div class="span2">
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
        % endif
    % endfor

<%def name="sidebar()">
    <%util:well>
        ${request.map.render()}
    </%util:well>
    <%util:well>
    <dl>
        <dt>Location</dt>
        <dd>
            ${u.format_coordinates(ctx)}
        </dd>
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
    </%util:well>
</%def>
