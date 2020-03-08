# -*- coding: utf-8 -*-
import time


URLS = [
    u'just=some&post=data',
    u'/some/path',
    u'http://example.com/foo',
    u'http://example.com/foo?a=1'
]

# lets have some creazy utf-8 key
KEYS = [u'1234', u'SFwje rhawuer'] # TODO u'♥ unicode ♥'

# checl different expire times are used
EXPIRES = [5, 60]

# check different times, including one bigger than 32 bit
TIMES = [0, int(time.time()), 2**33]
