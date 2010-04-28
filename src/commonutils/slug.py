# -*- coding: utf-8 -*-

import re


TR_DICT = {u'ç':'c', u'Ç':'C',
           u'ğ':'g', u'Ğ':'G',
           u'ı':'i', u'İ':'I',
           u'ö':'o', u'Ö':'O',
           u'ş':'s', u'Ş':'S',
           u'ü':'u', u'Ü':'U'}


SLUG_REMOVE_PAT = re.compile(r'[^\w\s]', re.MULTILINE)


def slugify(s, replace_dict = TR_DICT, length = 50):
    if not isinstance(s, unicode):
        s = unicode(s, 'utf-8')

    if len(s):
        s = s.strip()
        if replace_dict:
            for char in replace_dict:
                try:
                    s = s.replace(char, replace_dict[char])
                except:
                    s = s.replace(char, replace_dict[char].encode('utf-8'))
        s = s.lower()
        s = s.replace(' ', '-')
        s = s.replace('\n', '-')
        s = s.replace('\r', '-')
        s = SLUG_REMOVE_PAT.sub('-', s)

        # remove duplicate '-'
        while '--' in s:
            s = s.replace('--', '-')

        # remove '-' from the beginning and end
        # added: 5 Nov 2007
        if s and s[0] == '-':
            s = s[1:]
        if s and s[len(s)-1] == '-':
            s = s[:-1]

        # length = 0 means 'do not trim'
        if length:
            s = s[:length]

        # if the operation resulted in an empty string, use '-'
        if len(s) == 0:
            s = '-'

    return s.encode('utf-8')


def test():
    print slugify(u'ÖÇŞİĞÜ öçşığü')


if __name__ == '__main__':
    print slugify(u'ÖÇŞİĞÜ öçşığü')

