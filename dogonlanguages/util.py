from __future__ import unicode_literals
from math import floor

from six import text_type
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import icon
from clldutils.misc import format_size


def eol_link(req, species):
    if species.eol_url:
        return HTML.a(
            HTML.img(height=18, width=36, src=req.static_url('dogonlanguages:static/eol_logo.png')),
            href=species.eol_url,
            title="See related information at Encyclopedia Of Life (http://eol.org)")
    return ''


def cdstar_url(obj, type_='original'):
    return 'https://cdstar.shh.mpg.de/bitstreams/{0}/{1}'.format(
        obj.jsondata['objid'], obj.jsondata.get(type_) or obj.jsondata['original'])


def format_file(f):
    icon_ = {
        'image': 'camera',
        'video': 'facetime-video',
    }.get(f.mime_type.split('/')[0], 'file')
    label = ' [%s; %s]' % (f.mime_type, format_size(f.jsondata['size']))
    return HTML.span(icon(icon_, inverted=True), label, class_='badge')


def format_coordinates(obj):
    def degminsec(dec, hemispheres):
        _dec = abs(dec)
        degrees = int(floor(_dec))
        _dec = (_dec - int(floor(_dec))) * 60
        minutes = int(floor(_dec))
        _dec = (_dec - int(floor(_dec))) * 60
        seconds = _dec
        fmt = "{0}\xb0"
        if minutes:
            fmt += "{1:0>2d}'"
        if seconds:
            fmt += '{2:0>.2f}"'
        fmt += hemispheres[0] if dec > 0 else hemispheres[1]
        return text_type(fmt).format(degrees, minutes, seconds)

    lines = [
        '%s, %s;' % (degminsec(obj.latitude, 'NS'), degminsec(obj.longitude, 'EW')),
        '({0.latitude:.2f}, {0.longitude:.2f})'.format(obj),
    ]
    if getattr(obj, 'source_of_coordinates', None):
        lines.append('source: %s' % obj.source_of_coordinates)
    return ' '.join(lines)
