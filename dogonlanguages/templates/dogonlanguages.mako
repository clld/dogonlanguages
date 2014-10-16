<%inherit file="app.mako"/>

<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}"
       style="padding: 0;">
        <img width="42" src="${request.static_url('dogonlanguages:static/logo2.png')}"/>
    </a>
</%block>

${next.body()}
