# -*- coding: utf8 -*-
from logging import Logger, StreamHandler
import os

import django
from django.core.exceptions import ObjectDoesNotExist

from goldpoisk.product.models import Product as model, Material, Gem, Image, Type, Shop, Item

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goldpoisk.settings")
django.setup()

SHOP_ID = 1

class Product(object):
    def __init__(self, number, type_id, level=0):
        try:
            self.me = model.objects.get(number=number)
        except ObjectDoesNotExist as e:
            self.me = None

        self.type = Type.objects.get(pk=type_id)
        self.shop = Shop.objects.get(pk=SHOP_ID)
        self.logger = Logger('Product')
        self.logger.setLevel(level)
        self.logger.addHandler(StreamHandler())

    def update(self, data):
        self.logger.info('Updating %d %s' % (self.me.pk, self.me.number))
        product = self.me
        update = False

        if product.name != data['name']:
            #raise Exception(product.name, ':', data['name'])
            self.logger.error('Name:\n %s\n %s' % (product.name, data['name']))

        desc = data.get('description', None)
        if not self.match(product.description, desc):
            self.logger.debug('Desc:\n %s\n %s' % (product.description, desc))
            product.description = desc
            update = True

        weight = data.get('weight', None)
        if not self.match(product.weight, weight):
            self.logger.debug('Weight:\n %d\n %d' % (product.weight, weight))
            product.weight = weight
            update = True

        materials = data.get('material', '').split(',')
        for material in materials:
            m = self.get_material(material.capitalize())
            if not m in product.materials.all():
                self.logger.debug('Material: %s' % m.name)
                product.materials.add(m)
                update = True

        for gem in data.get('gems', []):
            g = self.get_gem(gem['name'], gem['carat'])
            if not g in product.gems.all():
                self.logger.debug('Gem: %s' % g.name)
                product.gems.add(g)
                update = True

        for src in data.get('images', []):
            if self.set_image(src, product):
                update = True

        assert(data['url'])
        if self.set_item(data['url'], product):
            update = True

        if not update:
            self.logger.info('No update')
        else:
            product.save()
            self.logger.info('Success')

    def get_material(self, material):
        try:
            return Material.objects.get(name__iexact=material)
        except ObjectDoesNotExist:
            m = Material.objects.create(name=material)
            m.save()
            return m

    def get_gem(self, name, carat):
        try:
            return Gem.objects.get(name__iexact=name, carat=carat)
        except ObjectDoesNotExist:
            gem = Gem.objects.create(name=name, carat=carat)
            gem.save()
            return gem

    def set_image(self, src, product):
        try:
            Image.objects.get(src=src)
            return False
        except ObjectDoesNotExist:
            self.logger.debug('Image %s' % src)
            image = Image.objects.create(src=src, product=product)
            image.save()
            return True

    def set_item(self, url, product):
        try:
            Item.objects.get(shop=self.shop, product=product)
            return False
        except ObjectDoesNotExist:
            self.logger.debug('Item: %s' % url)
            #TODO:
            item = Item.objects.create(**{
                'cost': 1000,
                'quantity': 1,
                'product': product,
                'shop': self.shop,
                'buy_url': url,
            })
            item.save()
            return True


    def create(self, data):
        self.logger.info('Creating %s' % data['number'])

        if self.me:
            raise Exception('Object exists', data['number'])

        assert data['name']
        assert data['weight']

        product = model.objects.create(**{
            'type': self.type,
            'name': data['name'],
            'number': data['number'],
            'description': data.get('description', 'Отстуствует'),
            'weight': data['weight'],
        })

        materials = data.get('material', '').split(',')
        for material in materials:
            m = self.get_material(material.capitalize())
            self.logger.debug('Material: %s' % m.name)
            product.materials.add(m)

        for gem in data.get('gems', []):
            g = self.get_gem(gem['name'], gem['carat'])
            self.logger.debug('Gem: %s' % g.name)
            product.gems.add(g)

        for src in data.get('images', []):
            self.set_image(src, product)

        assert(data['url'])
        self.set_item(data['url'], product)


    def match(self, db_field, field):
        if not field:
            return True

        return db_field == field
