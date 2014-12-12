from bs4 import BeautifulSoup as bs
import requests
from io import open

from clld.scripts.util import parsed_args


def get(args, relpath):
    cache = args.data_file('website', relpath)
    if not cache.exists():
        res = requests.get('http://dogonlanguages.org/' + relpath)
        with open(args.data_file('website', relpath), 'w', encoding='utf8') as fp:
            fp.write(res.text)
        return bs(res.text)


def parse(page, args, urls, level=0):
    page = get(args, page)
    if page:
        # scan links
        for link in page.find_all('a', href=True):
            href = link['href']
            if not href.startswith('http'):
                if href.endswith('.cfm'):
                    if level < 2:
                        parse(href, args, urls, level=level + 1)
                else:
                    if href.startswith('/'):
                        href = href[1:]
                    print href
                    urls[href] = 1


def main(args):
    urls = {}
    parse('index.cfm', args, urls)
    with open(args.data_file('website', 'urls.txt'), 'wb') as fp:
        for url in sorted(urls.keys()):
            fp.write('%s\n' % url)


if __name__ == '__main__':
    main(parsed_args())