#-*- coding: utf-8 -*-
import json
import copy
import logging
import math
import os
from PyV8 import JSArray
from time import time

from django.http import HttpResponse, Http404
from django.db.models import Min, Max

from goldpoisk import settings, js
from goldpoisk.product.models import Item, Type, Product
from goldpoisk.templates import get_menu, get_with_active_menu

logger = logging.getLogger('goldpoisk')

def category(req, category):
    logger.debug('Requestings category');
    cat = Type.objects.get(url=category)
    page = req.GET.get('page', 1)

    countPerPage = 30
    products, count = Product.get_by_category(category, page, countPerPage)

    json_list_url = req.path + '/json'
    #TODO: govnokot
    if req.is_ajax():
        res = HttpResponse(json.dumps({
            'category': cat.name,
            'count': count,
            'products': json.loads(products),
            'sortParams': [{
                'name': 'По алфавиту',
                'url': json_list_url + '?sort=name',
            }, {
                'name': 'Сначала дорогие',
                'url': json_list_url + '?sort=tprice',
            }, {
                'name': 'Сначала дешёвые',
                'url': json_list_url + '?sort=price',
            }],
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
        }))
        return res

    context = {
        'menu': JSArray(get_with_active_menu(category)),
        'category': cat.name,
        'count': count,
        'products': js.eval(products),
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
    html = js.render(context, 'pages.category')
    logger.info('Rendered %fs' % (time() - c))

    res = HttpResponse(html)
    return res

def best(req):
    logger.debug('Requesting best');
    page = req.GET.get('page', 1)

    countPerPage = 30
    products, count = Product.get_bids(page, countPerPage)
    context = {
        'menu': JSArray(get_menu()),
        'category': 'Лучшие предложения',
        'count': count,
        'products': js.eval(products),
        'paginator': {
            'totalPages': math.ceil(count / countPerPage) or 1,
            'currentPage': page,
            'url': req.path,
            'config': {
                'HTTP': {
                    'list': '#'
                }
            }
        }
    }

    html = js.render(context, 'pages.category')
    res = HttpResponse(html);
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

    html = js.render(context, 'pages.item')
    return HttpResponse(html)
