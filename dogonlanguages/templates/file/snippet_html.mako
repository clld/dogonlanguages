% if ctx.maintype == 'video':
    ${u.video_detail(ctx, autoplay='autoplay')|n}
% elif ctx.maintype == 'image':
    ${u.linked_image(ctx)|n}
% else:
    <p>No detailed view available</p>
% endif