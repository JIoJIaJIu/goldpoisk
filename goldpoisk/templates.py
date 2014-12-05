#-*- coding: utf8 -*-
import copy

from goldpoisk.product.models import Type

def mapMenu(item):
    return {
        'url': item.url,
        'type': item.type,
        'title': item.name
    }

MENU = map(mapMenu, Type.objects.all())

def get_with_active_menu(category): 
    menu = copy.deepcopy(MENU);
    for item in menu:
        if item.get('url') == category:
            item['isActive'] = True
    return menu

def get_menu_regexp():
    category = [x.get('url') for x in MENU]
    category_re = '^(?P<category>' + '|'.join(category) + ')$'
    return category_re

