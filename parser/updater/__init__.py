# -*- coding: utf8 -*-
import time
import re
import decimal
from logging import Logger, StreamHandler

import psycopg2

from . import config
from .product import Product
from .utils import Row, map_row, convert

class Database(object):
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect(database=config.POSTGRES_DATABASE,\
                                           user=config.POSTGRES_USER,\
                                           password=config.POSTGRES_PASSWORD)
        return self

    def __exit__(self, type, value, tb):
        self.connection.close()

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        return convert(cursor.description, rows)

    def get_infos(self):
        return self.execute("SELECT * FROM info WHERE parsed IS NULL")

class Updater(object):
    def __init__(self, db, info):
        self.logger = Logger("Updater")
        self.logger.setLevel(config.LOG_LEVEL)
        self.logger.addHandler(StreamHandler())

        self.logger.debug("Init %s", info)
        self.db = db
        self.schema = info.schema
        self.shop_id = config.get_shop_id(info.shop)
        self.logger.debug("Shema: %s", self.schema)
        self.logger.debug("SHOP_ID: %d", self.shop_id)

        sql = """
            SELECT *
            FROM %s.goldpoisk_entity
        """ % self.schema
        self.logger.info(sql)
        self.rows = [map_row(row) for row in self.db.execute(sql)]
        self.logger.debug("New items: %d", len(self.rows))

    def create_new_products(self):
        gem_sql = """
            SELECT name, weight
            FROM '%s'.goldpoisk_kamni
            WHERE article='%s'
            """ 

        images_sql = """
            SELECT src
            FROM %s.goldpoisk_entity_images
            WHERE article = '%s'
            """

        for row in self.rows:
            number = row['number']
            type_id = config.get_type(row['type'])
            product = Product(number, type_id, self.shop_id)

            '''
            cursor.execute(gem_sql % number)
            gems = cursor.fetchall()
            gems = self._convert_gems(gems)
            row['gems'] = gems
            '''

            images = self.db.execute(images_sql % (self.schema, number))
            row['images'] = [image.src for image in images]

            '''
            if product.me:
                product.update(row)
                continue
            product.create(row)
            '''

    def update_products(self):
        sql = """
            SELECT *
            FROM %s.goldpoisk_update_entity
        """ % self.schema
        
        self.logger.debug(sql)

        rows = self.db.execute(sql)
        self.logger.debug("To update items: %d", len(rows))
        for row in rows:
            type_id = config.get_type(row.category)
            product = Product(row.article, type_id, self.shop_id)
            key = row.fieldname
            value = row.fieldvalue
            d = dict([(key, value,)])
            product.update(d)

    # Private fields

    def _convert_gems(self, rows):
        d = []
        for row in rows:
            #TODO: hardcore
            carat = row[1].replace(',', '.')
            name = row[0].decode('utf-8').strip()

            if not carat:
                continue
            d.append({
                'name': name.capitalize(),
                'carat': decimal.Decimal(carat)
            })

        return d
