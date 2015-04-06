# -*- coding: utf8 -*-
import time
import re
import decimal

import MySQLdb as mdb
import psycopg2

from updater.product import Product
from updater.config import TYPE_ID, SHOP_ID

MYSQL_HOST = 'localhost'
MYSQL_USER_NAME = 'dev_goldpoisk'
MYSQL_USER_PASSWORD = 'dev12345'
MYSQL_DATABASE = 'goldpoisk_dump'

POSTGRES_DATABASE = 'dev_goldpoisk'
POSTGRES_USER = 'dev_goldpoisk'
POSTGRES_PASSWORD = 'dev12345'

class Row(object):
    def __init__(self, row, keys):
        self.row = row
        self.keys = keys

    def __getattr__(self, key):
        i = self.keys.index(key)
        data = self.row[i]
        if key == 'price' and data:
            data = re.sub(r'[^\d]', '', data)

        return data


class Updater(object):
    def __init__(self):
        self.rows = None

    def __enter__(self):
        self.mysql = mdb.connect(MYSQL_HOST, MYSQL_USER_NAME, MYSQL_USER_PASSWORD, MYSQL_DATABASE)
        self.postgres = psycopg2.connect(database=POSTGRES_DATABASE, user=POSTGRES_USER, password=POSTGRES_PASSWORD) 

        print "Entering.."
        current_time = time.time()
        sql = """
        SELECT *
        FROM goldpoisk_entity as entity
        """
        cursor = self.mysql.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        print "\tSpended time %fs" % (time.time() -  current_time)
        print "\tRows: %d" % len(rows)
        self.rows = self.convert(cursor.description, rows)
        return self

    def create_products(self):
        rows = self.rows
        gem_sql = """
        SELECT name, weight
        FROM goldpoisk_kamni
        WHERE article='%s'
        """

        images_sql = """
            SELECT src from goldpoisk_entity_images
            WHERE article = '%s'
            """

        cursor = self.mysql.cursor()
        for row in rows:
            number = row['number']
            product = Product(number, TYPE_ID)

            cursor.execute(gem_sql % number)
            gems = cursor.fetchall()
            gems = self.convert_gems(gems)
            row['gems'] = gems

            cursor.execute(images_sql % number)
            images = cursor.fetchall()
            row['images'] = self.convert_images(images)

            if product.me:
                product.update(row)
                continue
            product.create(row)

        cursor.close()

    def __exit__(self, type, value, tb):
        self.mysql.close()
        self.postgres.close()

    def price_hook(self):
        sql = """
        SELECT article, price, description
        FROM goldpoisk_other
        WHERE article='%s'
        """
        cursor = self.mysql.cursor()
        d = []
        for row in self.rows:
            cursor.execute(sql % row['number'])
            data = cursor.fetchall()
            if len(data) != 1:
                print('Length: %d' % len(data))
                print(row['number'])
                d.append(row['number'])
                continue

            data = data[0]
            product = Product(row['number'], TYPE_ID)
            data = {
                'price': int(data[1].replace('р.', '').strip()),
                'description': data[2].decode('utf-8'),
            }
            product.update_price(data['price'])
            product.update_desc(data['description'])

        cursor.close()
        print ', '.join(d)


    def _merge(self):
        print "Merging.."
        print "\tJOIN 2 mysql tables"
        current_time = time.time()
        sql = """
        SELECT article, name, material, weight, url
        FROM goldpoisk_entity as entity
        """
        m_cur = self.mysql.cursor()
        m_cur.execute(sql)
        rows = m_cur.fetchall()
        print "\tSpended time %fs" % (time.time() -  current_time)
        print "\tRows: %d" % len(rows)
        rows = self.convert(rows)

        self.create_products(rows)
        self.create_images(rows)
        self.create_items(rows)

    def _create_products(self, rows):
        cursor = self.postgres.cursor()
        for row in rows:
            # hack
            name = row.get('name').replace('тов', '').strip()
            article = row.get('article')
            #TODO:
            weight_reg = re.compile(r'\d+(\.\d+)?')
            weight = float(weight_reg.search(row.get('weight')).group(0))

            item = self.get_product_by_article(article)
            if not item:
                print "Inserting >", article
                sql ="""
                    INSERT INTO product_product
                    (type_id, name, number, description, weight) VALUES
                    (%d, '%s', '%s', 'Отсутсвует', %f)
                    """ % (TYPE_ID, name, article, weight)

                print sql
                cursor.execute(sql)
                item = self.get_product_by_article(article)
                self.postgres.commit()
            else:
                print "Founded >", article


            row['id'] = item[0]
        cursor.close()

    def _create_images(self, rows):
        print 'Create images..'
        current_time = time.time()

        images_sql = """
            SELECT src from goldpoisk_entity_images
            WHERE article = '%s'
            """
        p_images_sql = """
            SELECT src from product_image
            WHERE product_id = %d and src = '%s'
        """

        p_insert_sql = """
            INSERT INTO product_image
            (product_id, src) VALUES
            (%d, '%s')
        """

        m_cursor = self.mysql.cursor()
        p_cursor = self.postgres.cursor()
        for row in rows:
            m_cursor.execute(images_sql % row['article'])
            images = m_cursor.fetchall()
            print images
            for image in images:
                p_cursor.execute(p_images_sql % (row['id'], image[0]))
                if p_cursor.fetchone():
                    print '\tFounded >', image[0]
                else:
                    p_cursor.execute(p_insert_sql % (row['id'], image[0]))
                    print '\tInserted >', image[0]

        self.postgres.commit()
        p_cursor.close()
        print "Spended time %f" % (time.time() - current_time)

    def _create_items(self, rows):
        items_sql = """
            SELECT cost, quantity, product_id, shop_id, buy_url
            FROM product_item
            WHERE product_id = %d and shop_id = %d
            """
        insert_sql = """
            INSERT INTO product_item
            (cost, quantity, product_id, shop_id, buy_url) VALUES
            (%(cost)d, %(quantity)d, %(id)d, %(sid)d, '%(url)s')
            """

        cursor = self.postgres.cursor()
        for row in rows:
            cursor.execute(items_sql % (row['id'], SHOP_ID))
            items = cursor.fetchall()
            if items:
                print 'Founded',  len(items), row['id']
            else:
                cursor.execute(insert_sql % {
                    'cost': 1000,
                    'quantity': 1,
                    'id': row['id'],
                    'sid': SHOP_ID,
                    'url': row['url']
                })

        self.postgres.commit()
        cursor.close()

    def get_product_by_article(self, article):
        cursor = self.postgres.cursor()
        sql = """
            SELECT * from product_product
            WHERE number = '%s'
            """ % article
        cursor.execute(sql)
        item = cursor.fetchone()
        cursor.close()
        return item

    def convert(self, description, rows):
        d = []
        collumns = [q[0].decode('utf-8') for q in description]
        print '>>>', collumns, description

        for row in rows:
            row = Row(row, collumns)
            name = row.name.replace('тов', '')
            name = name.decode('utf-8').strip()
            price = row.price

            #TODO:
            weight_reg = re.compile(r'\d+(\.\d+)?')
            weight = 0
            if weight_reg.search(row.weight):
                weight = decimal.Decimal(weight_reg.search(row.weight).group(0))

            d.append({
                'number': row.article,
                'description': row.description.decode('utf-8'),
                'price': price or 0,
                'name': name,
                'material': row.material or '',
                'weight': weight,
                'url': row.url
            })
        return d

    def convert_gems(self, rows):
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

    def convert_images(self, images):
        d = []
        for img in images:
            img = img[0].decode('utf-8').strip()
            d.append(img)

        return d
