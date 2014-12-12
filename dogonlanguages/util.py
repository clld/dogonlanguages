from clld.web.util.htmllib import HTML


def eol_link(req, species):
    if species.eol_url:
        return HTML.a(
            HTML.img(height=18, width=36, src=req.static_url('dogonlanguages:static/eol_logo.png')),
            href=species.eol_url,
            title="See related information at Encyclopedia Of Life (http://eol.org)")
    return ''