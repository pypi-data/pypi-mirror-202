import re
import collections
import logging


tokenstate = collections.namedtuple('tokenstate', 'startpos endpos token')

logger = logging.getLogger(__name__)


class paragraph(object):
    '''a paragraph inside a man page is text that ends with two new lines'''

    def __init__(self, idx, text, section, is_option):
        self.idx = idx
        self.text = text
        self.section = section
        self.is_option = is_option

    def cleantext(self):
        t = re.sub(r'<[^>]+>', '', self.text)
        t = re.sub('&lt;', '<', t)
        t = re.sub('&gt;', '>', t)
        return t

    @staticmethod
    def from_store(d):
        p = paragraph(d.get('idx', 0), d['text'].encode(
            'utf8'), d['section'], d['is_option'])
        return p

    def to_store(self):
        return {'idx': self.idx, 'text': self.text, 'section': self.section,
                'is_option': self.is_option}

    def __repr__(self):
        t = self.cleantext()
        t = t[:min(20, t.find('\n'))].lstrip()
        return '<paragraph %d, %s: %r>' % (self.idx, self.section, t)

    def __eq__(self, other):
        if not other:
            return False
        return self.__dict__ == other.__dict__


class option(paragraph):
    '''a paragraph that contains extracted options

    short - a list of short options (-a, -b, ..)
    long - a list of long options (--a, --b)
    expectsarg - specifies if one of the short/long options expects an additional argument
    argument - specifies if to consider this as positional arguments
    nestedcommand - specifies if the arguments to this option can start a nested command
    '''

    def __init__(self, p, short, long, expectsargname, argument=None, nestedcommand=False):
        paragraph.__init__(self, p.idx, p.text, p.section, p.is_option)
        self.short = short
        self.long = long
        self._opts = self.short + self.long
        self.argument = argument
        self.expectsargname = expectsargname
        self.nestedcommand = nestedcommand
        if nestedcommand:
            assert expectsargname, 'an option that can nest commands must expect an argument'

    @property
    def opts(self):
        return self._opts

    '''
    @classmethod
    def from_store(cls, d):
        p = paragraph.from_store(d)

        return cls(p, d['short'], d['long'], d['expectsarg'], d['argument'],
                   d.get('nestedcommand'))

    def to_store(self):
        d = paragraph.to_store(self)
        assert d['is_option']
        d['short'] = self.short
        d['long'] = self.long
        d['expectsarg'] = self.expectsarg
        d['argument'] = self.argument
        d['nestedcommand'] = self.nestedcommand
        return d
    '''

    def __str__(self):
        return '(%s)' % ', '.join([str(x.flag) for x in self.opts])

    def __repr__(self):
        return '<options for paragraph %d: %s>' % (self.idx, str(self))


def extract(manpage):
    '''extract options from all paragraphs that have been classified as containing
    options'''
    for i, p in enumerate(manpage.paragraphs):
      #  print("%d"%i)
      #  print("%r"%p)
        if p.is_option:
           # print("%r"%p)
            s, l, endpos= extract_option(p.cleantext())
            if s or l:
                expectsarg = any(x.expectsarg for x in s + l)
                expectargname = None
                if expectsarg:
                    for x in s + l: #有的会出现 -d, --delimiter=DELIM的
                        if x.expectsarg:
                            expectargname = x.expectsarg
                    '''
                    for x in s + l:
                        if not x.expectsarg:
                            x.expectsarg = expectargname ?不能赋值
                    '''
                s = [x.flag for x in s]
                l = [x.flag for x in l]
                p.text = ' '.join(p.text[endpos:].split('.')[0].split('\n')) + ". "
                manpage.paragraphs[i] = option(p, s, l, expectargname)
            else:
                logger.info(
                    "no options could be extracted from paragraph %r", p)


opt_regex = re.compile(r'''
    (?P<opt>--?(?:\?|\#|(?:\w+-)*\w+))  # option starts with - or -- and can have - in the middle but not at the end, also allow '-?'
    (?:
     (?:[^\S\r\n]?(=)?[^\S\r\n]?)           # -a=
     (?P<argoptional>[<\[])?  # -a=< or -a=[
     (?:[^\S\r\n]?(=)?[^\S\r\n]?)           # or maybe -a<=
     (?P<arg>
      (?(argoptional)         # if we think we have an arg (we saw [ or <)
       [^\]>]+                # either read everything until the closing ] or >
       |
       (?(2)
        [-a-zA-Z]+             # or if we didn't see [ or < but just saw =, read all letters, e.g. -a=abc
        |
        [-a-z]+                # but if we didn't have =, only allow uppercase letters, e.g. -a FOO?????
       )
      )
     )
     (?(argoptional)(?P<argoptionalc>[\]>])) # read closing ] or > if we have an arg
    )?                        # the whole arg thing is optional
    (?P<ending>,\s*|\s+|\Z|/|\|)''', re.X)  # read any trailing whitespace or the end of the string

opt2_regex = re.compile(r'''
        (?P<opt>\w+)    # an option that doesn't start with any of the usual characters, e.g. options from 'dd' like bs=BYTES
        (?:
         (?:\s*=\s*)    # an optional arg, e.g. bs=BYTES
         (?P<arg>\w+)
        )
        (?:,\s*|\s+|\Z)''', re.X)  # end with , or whitespace or the end of the string


def _flag(s, pos=0):
    '''
    >>> _flag('a=b').groupdict()
    {'opt': 'a', 'arg': 'b'}
    >>> bool(_flag('---c-d'))
    False
    >>> bool(_flag('foobar'))
    False
    '''
    m = opt2_regex.match(s, pos)
    return m


def _option(s, pos=0):
    '''
    >>> bool(_option('-'))
    False
    >>> bool(_option('--'))
    False
    >>> bool(_option('---'))
    False
    >>> bool(_option('-a-'))
    False
    >>> bool(_option('--a-'))
    False
    >>> bool(_option('--a-b-'))
    False
    >>> sorted(_option('-a').groupdict().iteritems())
    [('arg', None), ('argoptional', None), ('argoptionalc', None), ('ending', ''), ('opt', '-a')]
    >>> sorted(_option('--a').groupdict().iteritems())
    [('arg', None), ('argoptional', None), ('argoptionalc', None), ('ending', ''), ('opt', '--a')]
    >>> sorted(_option('-a<b>').groupdict().iteritems())
    [('arg', 'b'), ('argoptional', '<'), ('argoptionalc', '>'), ('ending', ''), ('opt', '-a')]
    >>> sorted(_option('-a=[foo]').groupdict().iteritems())
    [('arg', 'foo'), ('argoptional', '['), ('argoptionalc', ']'), ('ending', ''), ('opt', '-a')]
    >>> sorted(_option('-a=<foo>').groupdict().iteritems())
    [('arg', 'foo'), ('argoptional', '<'), ('argoptionalc', '>'), ('ending', ''), ('opt', '-a')]
    >>> sorted(_option('-a=<foo bar>').groupdict().iteritems())
    [('arg', 'foo bar'), ('argoptional', '<'), ('argoptionalc', '>'), ('ending', ''), ('opt', '-a')]
    >>> sorted(_option('-a=foo').groupdict().iteritems())
    [('arg', 'foo'), ('argoptional', None), ('argoptionalc', None), ('ending', ''), ('opt', '-a')]
    >>> bool(_option('-a=[foo>'))
    False
    >>> bool(_option('-a=[foo bar'))
    False
    >>> _option('-a foo').end(0)
    3
    '''
    m = opt_regex.match(s, pos)
    if m:
        if m.group('argoptional'):
            c = m.group('argoptional')
            cc = m.group('argoptionalc')
            if (c == '[' and cc == ']') or (c == '<' and cc == '>'):
                return m
            else:
                return
    return m


_eatbetweenregex = re.compile(r'\s*(?:or|,|\|)\s*')


def _eatbetween(s, pos):
    '''
    >>> _eatbetween('foo', 0)
    0
    >>> _eatbetween('a, b', 1)
    3
    >>> _eatbetween('a|b', 1)
    2
    >>> _eatbetween('a or b', 1)
    5
    '''
    m = _eatbetweenregex.match(s, pos)
    if m:
        return m.end(0)
    return pos


class extractedoption(collections.namedtuple('extractedoption', 'flag expectsarg')):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.flag == other
        else:
            return super(extractedoption, self).__eq__(other)

    def __str__(self):
        return self.flag


def extract_option(txt):
    '''this is where the magic is (suppose) to happen. try and find options
    using a regex'''
    prepos = endpos = startpos = currpos = len(txt) - len(txt.lstrip())
    short, long = [], []

    m = _option(txt, currpos)

    # keep going as long as options are found
    while m:
        s = m.group('opt')
        po = extractedoption(s, m.group('arg'))
        # print("here%r",po.expectsarg)
        if s.startswith('--'):
            long.append(po)
        else:
            short.append(po)
        currpos = m.end(0)
        # print(m)
        # print(s)
        endpos = prepos + len(s)
        currpos = _eatbetween(txt, currpos)
        if m.group('ending') == '|':
            m = _option(txt, currpos)
            if not m:
                startpos = currpos
                while currpos < len(txt) and not txt[currpos].isspace():
                    if txt[currpos] == '|':
                        short.append(extractedoption(
                            txt[startpos:currpos], None))
                        startpos = currpos
                    currpos += 1
                leftover = txt[startpos:currpos]
                if leftover:
                    short.append(extractedoption(leftover, None))
                endpos = currpos
        else:
            m = _option(txt, currpos)
        prepos = currpos

    if currpos == startpos:
        m = _flag(txt, currpos)
        while m:
            s = m.group('opt')
            # print(s)
            po = extractedoption(s, m.group('arg'))
            long.append(po)
            endpos = prepos + len(s)
            currpos = _eatbetween(txt, currpos)
            m = _flag(txt, currpos)
            prepos = currpos

    return short, long, currpos

