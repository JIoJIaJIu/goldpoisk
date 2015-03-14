#-*- coding: utf-8 -*-
import copy
import os
import math
from PyV8 import JSArray
from pybem import pybem
from time import time

from django.http import HttpResponse, Http404
from django.db.models import Min, Max

from goldpoisk import settings
from goldpoisk.product.models import Item, Type, Product
from goldpoisk.templates import get_menu, get_with_active_menu

renderer = pybem.BEMRender(os.path.abspath(settings.TEMPLATE_DIRS[0]))

def category(req, category):
    _type = Type.objects.get(url=category)
    page = req.GET.get('page', 1)

    countPerPage = 30
    products, count = Product.get_by_category(category, page, countPerPage)

    json_list_url = req.path + '/list'
    context = {
        'menu': JSArray(get_with_active_menu(category)),
        'category': _type.name,
        'count': count,
        'products': products, #string
        #TODO:
        'sortParams': JSArray([{
            'name': 'По алфавиту',
            'url': json_list_url + '?sort=name',
        }, {
            'name': 'Сначала дорогие',
            'url': json_list_url + '?sort=tprice',
        }, {
            'name': 'Сначала дешёвые',
            'url': json_list_url + '?sort=price',
        }]),
        'paginator': {
            'totalPages': math.ceil(count / countPerPage) or 1,
            'currentPage': page,
            'url': req.path,
            'config': {
                'HTTP': {
                    'list': json_list_url
                }
            }
        }
    }

    c = time()
    html = renderer.render('index', context, req, 'pages.category')
    print 'Rendered %fs' % (time() - c)

    res = HttpResponse(html)
    return res

def product(req, id):
    try:
        product = Product.objects.prefetch_related('item_set').get(pk=id)
    except Product.DoesNotExist:
        raise Http404

    if not len(product.item_set.all()):
        raise Http404

    category = product.type
    images = product.image_set.all()

    # getting best item
    best_item = product.item_set.all()[0]
    context = {
        'menu': JSArray(get_with_active_menu(category.url)),
        'item': {
            'title': product.name,
            'category': product.type.name,
            'shop': best_item.shop.name,
            'shopUrl': best_item.shop.url,
            'buyUrl': best_item.buy_url,
            'price': best_item.cost,
            'gallery': {
                'images': JSArray(map(lambda i: i.get_absolute_url(), images)),
                'mainImg': images[0].get_absolute_url(),
            },
            'features': JSArray(product.get_features()),
            'description': product.description,
        },
    }

    html = renderer.render('index', context, req, 'pages.item')
    return HttpResponse(html)
