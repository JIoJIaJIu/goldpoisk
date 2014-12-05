#-*- coding: utf8 -*-
import os
import copy
from random import shuffle
from PyV8 import JSClass, JSArray
from pybem import pybem

from django.http import HttpResponse
from django.conf import settings

from goldpoisk.templates import get_menu
from goldpoisk.product.models import get_products_for_main

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

    context = {
        'menu': JSArray(get_menu()),
        'promo': promo,
        'products': JSArray(get_products_for_main()),
    }

    html = renderer.render('index', context, req, 'pages.index')
    res = HttpResponse(html);
    return res

