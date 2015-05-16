# -*- coding: utf8 -*-
from logging import Logger, StreamHandler
import os

import django
from django.core.exceptions import ObjectDoesNotExist

from goldpoisk.product.models import Product as model, Material, Gem, Image, Type, Shop, Item
from . import config

django.setup()

class Product(object):
    def __init__(self, number, type_id, shop_id):
        try:
            self.me = model.objects.get(number=number)
        except ObjectDoesNotExist as e:
            self.me = None

        self.type = Type.objects.get(pk=type_id)
        self.shop = Shop.objects.get(pk=shop_id)
        self.logger = Logger('Product')
        self.logger.setLevel(config.LOG_LEVEL)
        self.logger.addHandler(StreamHandler())

    def update(self, data):
        self.logger.info('Updating pk: %d number: %s' % (self.me.pk, self.me.number))
        product = self.me
        update = False

        name = data.get('name', None)
        if name and product.name != name:
            self.logger.error('Name:\n %s\n %s' % (product.name, name))

        desc = data.get('description', None)
        if desc and not self.match(product.description, desc):
            self.logger.debug('Desc:\n %s\n %s' % (product.description, desc))
            product.description = desc
            update = True

        weight = data.get('weight', None)
        if weight and not self.match(product.weight, weight):
            self.logger.debug('Weight:\n %d\n %d' % (product.weight, weight))
            product.weight = weight
            update = True

        materials = data.get('material', '').split(',')
        for material in materials:
            m = self.get_material(material.strip().capitalize())
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

        try:
            item = Item.objects.get(shop=self.shop, product=product)
            price = int(data.get('price', 0))
            if price and item.cost != price:
                item.cost = price
                item.save()
                self.logger.info("Item price: %s", price)

            count = int(data.get('count', 0))
            if count != item.quantity:
                item.quantity = count
                item.save()
                self.logger.info("Item count: %s", count)
        except ObjectDoesNotExist:
            assert(data['url'])
            if self.set_item(data['url'], data['price'], product):
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

    def set_item(self, url, price, product):
        try:
            Item.objects.get(shop=self.shop, product=product)
            return False
        except ObjectDoesNotExist:
            self.logger.debug('Item: %s' % url)
            #TODO:
            item = Item.objects.create(**{
                'cost': price,
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

        product = model.objects.create(**{
            'type': self.type,
            'name': data['name'],
            'number': data['number'],
            'description': data.get('description') or '',
            'weight': data['weight'],
        })

        materials = data.get('material', '').split(',')
        for material in materials:
            m = self.get_material(material.strip().capitalize())
            self.logger.debug('Material: %s' % m.name)
            product.materials.add(m)

        for gem in data.get('gems', []):
            g = self.get_gem(gem['name'], gem['carat'])
            self.logger.debug('Gem: %s' % g.name)
            product.gems.add(g)

        for src in data.get('images', []):
            self.set_image(src, product)

        assert(data['url'])
        self.set_item(data['url'], data['price'], product)


    #HACK
    def update_price(self, price):
        if not self.me:
            raise Exception('No product')

        item = Item.objects.get(shop=self.shop, product=self.me)

        if item.cost == price:
            return

        item.cost = price
        item.save()
        self.logger.debug('Price: %d' % price)

    #HACK
    def update_desc(self, desc):
        if not self.me:
            raise Exception('No product')

        if not desc:
            return

        if self.me.description == desc:
            return

        self.me.description = desc
        self.me.save()
        self.logger.debug('Price: %s' % desc)

    def match(self, db_field, field):
        if not field:
            return True

        return db_field == field
