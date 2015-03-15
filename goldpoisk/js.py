# -*- coding: utf-8 -*-
from PyV8 import JSContext, JSLocker

import os
import re

from django.conf import settings

JS_ESCAPABLE = re.compile(r'([^\x00-\x7f])')
HAS_UTF8 = re.compile(r'[\x80-\xff]')

def _js_escape_unicode_re_callack(match):
    n = ord(match.group(0))
    if n < 0x10000:
        return '\\u%04x' % (n,)
    else:
        # surrogate pair
        n -= 0x10000
        s1 = 0xd800 | ((n >> 10) & 0x3ff)
        s2 = 0xdc00 | (n & 0x3ff)
        return '\\u%04x\\u%04x' % (s1, s2)


def js_escape_unicode(text):
    """Return an ASCII-only representation of a JavaScript string"""
    if isinstance(text, str):
        if HAS_UTF8.search(text) is None:
            return text

        text = text.decode('UTF-8')

    return str(JS_ESCAPABLE.sub(_js_escape_unicode_re_callack, text))

dirname = os.path.abspath(settings.TEMPLATE_DIRS[0])
files = map(lambda x: open(os.path.join(dirname, x)).read(), ['index/index.bemhtml.js', 'index/index.priv.js'])
files = map(lambda x: js_escape_unicode(x), files)

def render (data, entry_point, bemjson=False, env=None):
    with JSLocker():
        with JSContext() as c:
            c.eval("\n".join(files))
            c.locals.context = data;
            c.locals.env = env;
            if bemjson:
                return c.eval('JSON.stringify(%s(context, env))' % entry_point)

            return c.eval('BEMHTML.apply(%s(context, env))' % entry_point)

