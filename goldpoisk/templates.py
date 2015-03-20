#-*- coding: utf-8 -*-
import os
import logging
from time import time

from django.conf import settings

from goldpoisk.product.models import Type

logger = logging.getLogger('goldpoisk')

def get_menu():
    return map(map_menu, Type.objects.all().order_by('pk'))

def get_with_active_menu(category): 
    menu = get_menu();
    for item in menu:
        if item.get('href') == category:
            item['isActive'] = True
    return menu

def get_menu_regexp(at_end=''):
    category = [x.get('href') for x in get_menu()]
    category_re = '^(?P<category>' + '|'.join(category) + ')' + at_end + '$'
    return category_re

def map_menu(item):
    return {
        'href': item.url,
        'type': item.type,
        'label': item.name
    }
