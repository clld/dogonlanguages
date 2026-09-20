from math import floor
import mimetypes

from clld.db.models.common import Source
from clld.web.util.htmllib import HTML, literal
from clld.web.util.helpers import icon, link
from clldutils import misc

from dogonlanguages.models import Movie
from .cdstar2s3 import MAPPING

ICON_FOR_MIMETYPE = {
    'facetime-video': [
        'video',
    ],
    'camera': [
        'image',
    ],
    'headphones': [
        'audio',
    ],
    'file': [
        'text',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ],
    'list': [
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/csv',
    ],
}
MIMETYPE_TO_ICON = {}
for icon_, types_ in ICON_FOR_MIMETYPE.items():
    for type_ in types_:
        MIMETYPE_TO_ICON[type_] = icon_


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
        HTML.td(*[HTML.a(format_file(f), href=bitstream_url(f)) for f in doc._files])
    )


def bitstream_url(obj, type_='original'):
    try:
        fname = MAPPING['-'.join([obj.jsondata['objid'], obj.jsondata[type_] or obj.jsondata['original']])]
    except:
        print(obj.jsondata)
        raise
    return "https://s3.nexus.mpcdf.mpg.de/eva-dlce-dogonlanguages/" + fname


def linked_image(obj):
    return HTML.a(
        HTML.img(src=bitstream_url(obj, 'web'), class_='image'),
        href=bitstream_url(obj),
        title=f"View image ({format_size(obj)})")


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
        *[HTML.li(HTML.a(' ' + format_file(f), href=bitstream_url(f))) for f in fs],
        **dict(class_='unstyled'))


def vlink(obj, label=None):
    label = label or 'View file'
    mtype = mimetype(obj)
    icon_ = MIMETYPE_TO_ICON.get(
        mtype, MIMETYPE_TO_ICON.get('video', 'download-alt'))
    md = ''
    if obj.jsondata.get('size'):
        md = format_size(obj)
    if md:
        md += ', '
    md += mtype
    if md:
        label += ' (%s)' % md
    return HTML.a(
        HTML.span(
            icon(icon_),
            ' ' + label,
            class_='cdstar_link'),
        href=bitstream_url(obj))


def mimetype(obj):
    if hasattr(obj, 'mimetype'):
        return obj.mimetype
    if hasattr(obj, 'mime_type'):
        return obj.mime_type
    for key in [
        'mediaType',  # CLDF property name
        'Media_Type',  # CLDF default column name
        'mimetype',
        'mime_type',
    ]:
        if obj.jsondata.get(key):
            return obj.jsondata[key]
    return mimetypes.guess_type(obj.jsondata['original'])[0] or 'application/octet-stream'


def video_detail(*objs, **kw):
    def video(mp4, **kw):
        kw.update(width='100%', preload='none')
        if mp4.jsondata.get('thumbnail'):
            kw['poster'] = bitstream_url(mp4, type_='thumbnail')
        label = kw.pop('label', None)
        kw.setdefault('controls', 'controls')
        media_element = getattr(HTML, 'video')(
            literal(f'Your browser does not support the <code>video</code> element.'),
            HTML.source(src=bitstream_url(mp4, type_='web'), type=mimetype(mp4)), **kw)
        return HTML.div(
            media_element,
            HTML.br(),
            vlink(mp4, label=label),
            class_=f'cdstar_video_link',
            style='margin-top: 10px')

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
