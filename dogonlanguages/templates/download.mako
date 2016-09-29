<%inherit file="home_comp.mako"/>

<h3>Downloads</h3>

<div class="span5 well well-small">
    <dl>
    % for model, dls in h.get_downloads(request):
        <dt>${_(model)}</dt>
        % for dl in dls:
        <dd>
            <a href="${dl.url(request)}">${dl.label(req)}</a>
        </dd>
        % endfor
    % endfor
    </dl>
</div>
<div class="span6">
    <p>
        In addition to the downloads listed here, there are numerous downloadable materials
        attached to
        <a href="${request.route_url('sources')}">items in the bibliography</a>
        or listed on the
        <a href="${request.route_url('files')}">"Files" page</a>.
    </p>
    <p>
        Downloads are provided as
        ${h.external_link("http://en.wikipedia.org/wiki/Zip_%28file_format%29", label="zip archives")}
        bundling the data and a
        ${h.external_link("http://en.wikipedia.org/wiki/README", label="README")}
        file.
    </p>
</div>