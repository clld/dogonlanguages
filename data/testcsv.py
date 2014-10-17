from clld.lib.dsv import reader


def main():
    p = 'dogon_lexicon_test.csv'
    for p in zip(*list(reader(p, delimiter=',', escapechar='\\'))):
        print p



if __name__ == '__main__':
    main()