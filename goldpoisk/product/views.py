#-*- coding: utf-8 -*-
import json
import copy
import logging
import math
import os
from PyV8 import JSArray
from time import time

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.db.models import Min, Max

from goldpoisk import settings, js
from goldpoisk.ajax.views import GET_int
from goldpoisk.product.models import Item, Type, Product, get_filters
from goldpoisk.product.models import ProductSerializer
from goldpoisk.templates import get_menu, get_with_active_menu, get_env

logger = logging.getLogger('goldpoisk')

def category(req, category):
    logger.debug('Requestings category');
    cat = Type.objects.get(url=category)
    page = req.GET.get('page', 1)
    filters = {
        'gems': GET_int(req, 'gem'),
        'shops': GET_int(req, 'store'),
        'materials': GET_int(req, 'material'),
    }

    countPerPage = 30
    products, count = Product.get_by_category(category, page, countPerPage, filters=filters)

    json_list_url = req.path + '/json'

    context = {
        'menu': get_with_active_menu(category),
        'category': cat.name,
        'count': count,
        'products': json.loads(products),
        'sortParams': [{
            'name': 'По алфавиту',
            'value': 'name'
        }, {
            'name': 'Сначала дорогие',
            'value': 'tprice'
        }, {
            'name': 'Сначала дешёвые',
            'value': 'price'
        }],
        'paginator': {
            'totalPages': math.ceil(float(count) / countPerPage) or 1,
            'currentPage': page,
            'url': req.path,
            'config': {
                'HTTP': {
                    'list': json_list_url
                }
            }
        },
        "filters": get_filters(cat),
    }

    if req.is_ajax():
        return HttpResponse(json.dumps(context))

    c = time()
    html = js.render(json.dumps(context), 'pages["category.json"]', env=get_env())
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
            'totalPages': math.ceil(float(count) / countPerPage) or 1,
            'currentPage': page,
            'url': req.path,
            'config': {
                'HTTP': {
                    'list': '#'
                }
            }
        }
    }

    html = js.render(context, 'pages.category', env=get_env())
    res = HttpResponse(html);
    return res

def product(req, slug):
    try:
        product = Product.objects.prefetch_related('item_set').get(slug__exact=slug)
    except Product.DoesNotExist:
        raise Http404

    items = product.item_set.all()
    if not len(items):
        raise Http404

    if (req.is_ajax()):
        product = ProductSerializer().serialize(product)
        return HttpResponse(product, 'application/json')

    context = {
        'menu': JSArray(get_menu()),
        'item': product.json(),
    }

    html = js.render(context, 'pages["item.json"]', env=get_env())
    return HttpResponse(html)

def products(req):
    if not req.is_ajax():
        raise Http404

    ids = req.GET.get('ids', "").split('.')
    try:
        print ids, req.GET
        ids = map(lambda x: x and int(x), ids)
    except:
        return HttpResponse('Wrong parameter %s' % ids, status=404, content_type="application/json")

    products = Product.objects.filter(id__in=ids)

    #TODO
    l = []
    for i in products:
        product = json.loads(ProductSerializer().serialize(i))
        item = i.item_set.first()
        product.update({
            'jsonUrl': i.get_absolute_url() + '/json',
            'shopName': item.shop.name,
            'shopUrl': item.shop.url,
            'buyUrl': item.buy_url,
            'minPrice': item.cost,
            'carat': i.get_carat(),
            'image': i.image_set.first().get_absolute_url(),
            'count': 1
        })
        l.append(product)

    dump = json.dumps({
        'count': len(products),
        'list': l,
    })
    return HttpResponse(dump, content_type="application/json")

def search(req):
    if not req.is_ajax():
        raise Http404

    number = req.GET.get('article', None)
    if not number:
        return HttpResponse('Should point article', status=403, content_type="application/json")

    try:
        product = Product.objects.get(number=number)
        return HttpResponse(product.json())
    except ObjectDoesNotExist:
        return HttpResponse('%s: no such product' % number, status=404, content_type="application/json")
