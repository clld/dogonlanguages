<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "movies" %>
<%block name="title">Documentary video: ${ctx.name}</%block>

<h2>${ctx.name}</h2>

${u.video_detail(ctx)}