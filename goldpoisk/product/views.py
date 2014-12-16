import copy
import os
from PyV8 import JSArray
from pybem import pybem

from django.http import HttpResponse, Http404
from django.db.models import Min, Max

from goldpoisk import settings
from goldpoisk.product.models import Item, Type, Product, get_products_for_category
from goldpoisk.templates import get_menu, get_with_active_menu

renderer = pybem.BEMRender(os.path.abspath(settings.TEMPLATE_DIRS[0]))

def category(req, category):
    #TODO:
    type = Type.objects.get(url=category)
    products = get_products_for_category(category)
    count = len(products)

    context = {
        'menu': JSArray(get_with_active_menu(category)),
        'category': type.name,
        'count': len(products),
        'products': JSArray(products)
    }

    html = renderer.render('index', context, req, 'pages.category')

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
