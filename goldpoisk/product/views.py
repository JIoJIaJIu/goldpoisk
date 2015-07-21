#-*- coding: utf-8 -*-
import json
import copy
import logging
import math
import os
from PyV8 import JSArray
from time import time

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404
from django.db.models import Min, Max

from goldpoisk import settings, js
from goldpoisk.utils import to_int, to_string
from goldpoisk.serializer import CustomsProductSerializer
from goldpoisk.ajax.views import GET_int
from goldpoisk.product.models import Item, Type, Product, get_filters
from goldpoisk.product.models import ProductSerializer
from goldpoisk.product.models import generate_title, generate_description
from goldpoisk.templates import get_menu, get_with_active_menu, get_env

logger = logging.getLogger('goldpoisk')

"""
Controller on requesting through raw GET request category
Also it works for AJAX requests
"""
def category(req, category):
    logger.debug('Requestings category %s' % req.path);
    cat = Type.objects.get(url=category)
    page_number = to_int(req.GET.get('page'), 1)
    sort_key = to_string(req.GET.get('sort'), None)

    filters = {
        'gems': GET_int(req, 'gem'),
        'shops': GET_int(req, 'store'),
        'materials': GET_int(req, 'material'),
    }

    products = Product.customs.filter(type__url__exact=category)
    products = products.filter_by_gems(filters['gems'])\
                       .filter_by_shops(filters['shops'])\
                       .filter_by_materials(filters['materials'])\
                       .sort(sort_key)

    paginator = Paginator(products, 30)
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(1)
    serializer = CustomsProductSerializer()

    context = {
        'menu': get_with_active_menu(category),
        'category': cat.name,
        'count': paginator.count,
        'products': map(lambda p: serializer.normalize(p), page.object_list),
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
            'totalPages': paginator.num_pages,
            'currentPage': page.number,
            'url': req.path,
            'config': {
                'HTTP': {
                    'list': req.path + '/json'
                }
            }
        },
        "filters": get_filters(cat),
    }

    if req.is_ajax():
        return HttpResponse(json.dumps(context), content_type="application/json")

    c = time()
    html = js.render(json.dumps(context), 'pages["category.json"]', env=get_env())
    logger.info('Rendered %fs' % (time() - c))

    res = HttpResponse(html)
    return res

"""
Controller that works only through AJAX
For sorting
"""
def sort(req, category):
    logger.debug('Request sorting %s' % req.path)
    if not req.is_ajax():
        raise Http404

    page_number = to_int(req.GET.get('page'), 1)
    sort_key = to_string(req.GET.get('sort'), None)

    filters = {
        'gems': GET_int(req, 'gem'),
        'shops': GET_int(req, 'store'),
        'materials': GET_int(req, 'material'),
    }

    products = Product.customs.filter(type__url__exact=category)
    products = products.filter_by_gems(filters['gems'])\
                       .filter_by_shops(filters['shops'])\
                       .filter_by_materials(filters['materials'])\
                       .sort(sort_key)

    paginator = Paginator(products, 30)
    try:
        page = paginator.page(page_number)
    except:
        page = paginator.page(1)
    serializer = CustomsProductSerializer()

    products = json.dumps({
        'list': map(lambda x: serializer.normalize(x), page.object_list),
        'count': paginator.count,
    })
    return HttpResponse(products, 'application/json')

"""
Controller that works only through plain GET request
Return bids page
"""
def best(req):
    logger.debug('Requesting best');
    page = to_int(req.GET.get('page'), 1)

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

    #TODO: merge
    if (req.is_ajax()):
        context = {
            'title': generate_title(product),
            'description': generate_description(product),

            #breadcrumbs
            'name': product.name,
            'category': product.type.name,
            'categoryUrl': "/%s" % product.type.url,

            'item': json.loads(product.json())
        }
        return HttpResponse(json.dumps(context), 'application/json')

    context = {
        'title': generate_title(product),
        'description': generate_description(product),

        #breadcrumbs
        'name': product.name,
        'category': product.type.name,
        'categoryUrl': "/%s" % product.type.url,

        'menu': JSArray(get_menu()),
        'item': product.json(),
    }

    html = js.render(context, 'pages["item.json"]', env=get_env())
    return HttpResponse(html)

def products(req):
    if not req.is_ajax():
        raise Http404

    ids = GET_int(req, 'ids')
    ids.reverse()
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
