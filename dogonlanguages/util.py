from math import floor

from clld.db.models.common import Source
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import icon, link
from clldutils import misc
from clldmpg import cdstar

from dogonlanguages.models import Movie


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


def format_document_link(req, doc, label):
    return HTML.tr(
        HTML.td(link(req, doc, label=label)),
        HTML.td(*[HTML.a(format_file(f), href=cdstar_url(f)) for f in doc._files])
    )


cdstar_url = cdstar.bitstream_url


def linked_image(obj):
    return cdstar.linked_image(obj, check=False)


def format_size(f):
    return misc.format_size(f.jsondata['size'])


def format_duration(f):
    if f.duration:
        return "%d:%02d" % divmod(f.duration, 60)
    return ''


def format_file(f, with_mime_type=True):
    icon_ = {
        'image': 'camera',
        'video': 'facetime-video',
    }.get(f.mime_type.split('/')[0], 'file')
    if with_mime_type:
        label = f.mime_type + '; '
    else:
        label = ''
    label = ' [%s%s]' % (label, misc.format_size(f.jsondata['size']))
    return HTML.span(icon(icon_, inverted=True), label, class_='badge')


def format_videos(fs):
    return HTML.ul(
        *[HTML.li(HTML.a(' ' + format_file(f), href=cdstar_url(f))) for f in fs],
        **dict(class_='unstyled'))


def video_detail(*objs, **kw):
    def video(mp4):
        return cdstar.video(mp4, width='100%', preload='none', **kw)

    mp4s, name, dl = [], None, []
    if isinstance(objs[0], Movie):
        dl.extend([HTML.dt('Description'), HTML.dd(objs[0].name)])
        dl.extend([HTML.dt('Duration'), HTML.dd(format_duration(objs[0]))])
        if objs[0].get_file('mp4'):
            mp4s = [objs[0].get_file('mp4')]
        files = objs[0].files
    else:
        for obj in objs:
            if obj.mime_type == 'video/mp4':
                mp4s.append(obj)
        files = objs
    dl.extend([HTML.dt('Formats'), HTML.dd(format_videos(files))])
    return HTML.div(
        HTML.ul(*[HTML.li(video(mp4)) for mp4 in mp4s], **dict(class_='unstyled')),
        HTML.dl(*dl))


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
        return str(fmt).format(degrees, minutes, seconds)

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
