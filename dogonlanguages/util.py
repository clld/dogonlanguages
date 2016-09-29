from __future__ import unicode_literals
from math import floor

from six import text_type
from clld.db.models.common import Source
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import icon
from clldutils import misc


def tsammalex_link(request, concept):
    if not concept.tsammalex_taxon:
        return ''
    return HTML.a(
        HTML.img(
            src=request.static_url('dogonlanguages:static/tsamma.png'),
            height=20,
            width=30),
        title='corresponding taxon at Tsammalex',
        href=concept.tsammalex_url)


def concepticon_link(request, concept):
    if not concept.concepticon_id:
        return ''
    return HTML.a(
        HTML.img(
            src=request.static_url('dogonlanguages:static/concepticon_logo.png'),
            height=20,
            width=30),
        title='corresponding concept set at Concepticon',
        href=concept.concepticon_url)


def cdstar_url(obj, type_='original'):
    return 'https://cdstar.shh.mpg.de/bitstreams/{0}/{1}'.format(
        obj.jsondata['objid'], obj.jsondata.get(type_) or obj.jsondata['original'])


def linked_image(f):
    return HTML.a(
        HTML.img(src=cdstar_url(f, 'web'), class_='image'),
        href=cdstar_url(f),
        title="view image [{0}]".format(format_size(f)))


def format_size(f):
    return misc.format_size(f.jsondata['size'])


def format_file(f):
    icon_ = {
        'image': 'camera',
        'video': 'facetime-video',
    }.get(f.mime_type.split('/')[0], 'file')
    label = ' [%s; %s]' % (f.mime_type, misc.format_size(f.jsondata['size']))
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


def language_index_html(context=None, request=None, **kw):
    return {
        'refs': {
            k: Source.get(misc.slug(k)) for k in
            'Hochstetler_etal2004 Blench2007 Blench2005 Blench2005b Blench2007b'.split()}}


def value_index_html(context=None, request=None, **kw):
    ids = 'heathetal2015 floradogonunicode faunadogonunicode'.split()
    return {
        'spreadsheets': [Source.get(sid) for sid in ids],
        'heathmcpherson2009actionverbs': Source.get('heathmcpherson2009actionverbs')
    }
