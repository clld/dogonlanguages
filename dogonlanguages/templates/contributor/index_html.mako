<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributors" %>
<%block name="title">${_('Contributors')}</%block>


<h2>${_('Contributors')}</h2>

${ctx.render()}
