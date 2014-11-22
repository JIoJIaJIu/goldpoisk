#-*- coding: utf8 -*-
from django.http import HttpResponse
from django.conf import settings
import os

from PyV8 import JSClass, JSArray
from pybem import pybem
from  goldpoisk import templates

class JS(JSClass):
    def log(self, *args):
        print args

renderer = pybem.BEMRender(os.path.abspath(settings.TEMPLATE_DIRS[0]), toplevelcls=JS)

def main(req):
    html = renderer.render('index', {
        'menu': templates.MENU,
        'promo': ['','', ''],
        'css': JSArray([])
    }, req, 'blocks.page');
    res = HttpResponse(html);
    return res
