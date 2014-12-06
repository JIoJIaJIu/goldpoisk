#-*- coding: utf-8 -*-
from goldpoisk.product.models import Type

def get_menu():
    return map(mapMenu, Type.objects.all())

def get_with_active_menu(category): 
    menu = get_menu();
    for item in menu:
        if item.get('href') == category:
            item['isActive'] = True
    return menu

def get_menu_regexp():
    category = [x.get('href') for x in get_menu()]
    category_re = '^(?P<category>' + '|'.join(category) + ')$'
    return category_re

def mapMenu(item):
    return {
        'href': item.url,
        'type': item.type,
        'label': item.name
    }

