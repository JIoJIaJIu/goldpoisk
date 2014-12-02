#-*- coding: utf8 -*-
from django.http import HttpResponse
from django.conf import settings
import os
import copy

from PyV8 import JSClass, JSArray
from pybem import pybem
from  goldpoisk import templates

from random import shuffle

class JS(JSClass):
    def log(self, *args):
        print args

renderer = pybem.BEMRender(os.path.abspath(settings.TEMPLATE_DIRS[0]), toplevelcls=JS)

def main(req):
    promo = [
        'media/promotion/promotion_01.jpg',
        'media/promotion/promotion_02.jpg',
        'media/promotion/promotion_03.jpg',
    ]
    shuffle(promo)


    content = renderer.render('index', {
        'promo': promo
    }, req, 'blocks["g-content.index"]', return_bemjson=True)

    html = renderer.render('index', {
        'menu': JSArray(templates.MENU),
        'content': content
    }, req, 'blocks.page')
    res = HttpResponse(html);
    return res

def category(req, category):
    menu = copy.deepcopy(templates.MENU);
    for item in menu:
        if item['type'] == category:
            item['isActive'] = True

    html = renderer.render('index', {
        'menu': JSArray(menu),
    }, req, 'blocks.page')

    res = HttpResponse(html);
    return res
