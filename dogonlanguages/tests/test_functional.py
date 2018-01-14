import pytest

pytest_plugins = ['clld']


@pytest.mark.parametrize(
    "method,path",
    [

        ('get_html', '/'),
        ('get_dt', '/contributors'),
        ('get_dt', '/thesaurus.cfm'),
        ('get_dt', '/values'),
        ('get_dt', '/languages.cfm'),
        ('get_dt', '/bibliography.cfm'),
        ('get_dt', '/geography.cfm'),
        ('get_html', '/contributors'),
        ('get_html', '/thesaurus.cfm'),
        ('get_html', '/values'),
        ('get_html', '/languages.cfm'),
        ('get_html', '/bibliography.cfm'),
        ('get_html', '/geography.cfm'),
        ('get_html', '/villages/638'),
        ('get_json', '/geography.cfm.geojson'),
        ('get_html', '/villages/1002'),
        ('get_html', '/typology'),
        ('get_html', '/parameters/60591'),
        ('get_html', '/parameters/50283'),
        ('get_html', '/parameters/01767'),
        ('get_html', '/parameters/60037'),
        ('get_json', '/parameters/01767.geojson'),
        ('get_html', '/other'),
        ('get_html', '/florafauna.cfm'),
        ('get_html', '/bangime.cfm'),
        ('get_html', '/movies'),
        ('get_dt', '/movies'),
        ('get_html', '/languages/ampa1238'),
        ('get_json', '/languages/ampa1238.geojson'),
        ('get_dt', '/values?parameter=00001'),
        ('get_dt', '/values?language=ampa1238'),
        ('get_html', '/contributions/d'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
