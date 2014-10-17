import re
from hashlib import md5

from clld.lib.bibtex import Database, Record


KV_PATTERN = re.compile('(?P<key>[A-Za-z]+)\s*\=\s*\{(?P<value>.*)$', re.MULTILINE)


def fixed(mess):
    id_ = md5('@' + mess.encode('utf8'))
    for messyid in ['BibTeX', 'Indiana University']:
        mess = mess.replace(messyid + ',\n', '')
    genre, rem = mess.split('{', 1)
    assert rem.endswith('}')
    rem = rem[:-1].strip()
    kw = {}
    for kv in re.split('},\n', rem):
        kv = kv.strip()
        if kv.endswith('}'):
            kv = kv[:-1]
        m = KV_PATTERN.match(kv)
        if not m:
            #print kv
            continue
        kw[m.group('key')] = m.group('value')
    rec = Record(genre, id_.hexdigest(), **kw)
    print rec
    return rec


def main(records):
    new = []
    for record in records:
        if not record.strip():
            continue
        new.append(fixed(record.strip()))

    db = Database(new)


if __name__ == '__main__':
    main(open('refs.bib').read().decode('utf8').split('\n@'))
