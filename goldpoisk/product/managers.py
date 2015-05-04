from django.db import models
from django.db.models import Lookup
from django.db.models import QuerySet, Count, Min, Max, F

class ProductQuerySet(models.QuerySet):
    def filter_by_gems(self, ids):
        if not ids:
            return self

        if not len(ids):
            return self

        return self.filter(gems__id__in=ids)

    def filter_by_materials(self, ids):
        if not ids:
            return self

        if not len(ids):
            return self

        return self.filter(materials__id__in=ids)

    def filter_by_shops(self, ids):
        if not ids:
            return self

        if not len(ids):
            return self

        return self.filter(item__shop__id__in=ids)

    def sort(self, key):
        if not key:
            return self

        sort_fn = {
            'price': lambda products: products.order_by('min_cost'),
            'tprice': lambda products: products.order_by('-max_cost'),
            'name': lambda products: products.order_by('name'),
        }[key]
        if sort_fn:
            return sort_fn(self)

        return self

class ProductManager(models.Manager):
    def get_queryset(self):
        query = ProductQuerySet(self.model, using=self._db)
        query = query.filter(item__isnull=False)
        query = query.annotate(count=Count('item'))
        query = query.annotate(min_cost=Min('item__cost'), max_cost=Max('item__cost'))
        query = query.annotate(action=Count('item__action'), hit=Count('item__hit'), bestbid=Count('item__bestbid'))
        return query

    def all_by_category(self, category, page=1, countPerPage=30, sort=None):
        try:
            page = int(page)
        except:
            page = 1
        ORDER_BY = ''
        OFFSET = ''

        if sort:
            ORDER_BY = {
                'name': 'ORDER BY p.name',
                'price': 'ORDER BY cost',
                'tprice': 'ORDER BY cost DESC',
            }[sort] or ''

        if page != 1:
            print countPerPage * page
            OFFSET = 'OFFSET %d' % (countPerPage * page)

        items_sql = """
            SELECT p.id, p.name, p.slug, p.description, p.weight,
                   i.cost as cost, i.buy_url,
                   i.shop_id
            FROM
                (
                    SELECT p.id, p.name, p.slug, p.description,
                           p.number, p.weight

                    FROM %(product_table)s as p

                    INNER JOIN %(type_table)s as t
                    ON p.type_id = t.id
                    WHERE t.url = '%(category)s'
                ) as p

            INNER JOIN %(item_table)s as i
            ON i.product_id = p.id

        """ % {
            'type_table': 'product_type',
            'product_table': 'product_product',
            'item_table': 'product_item',
            'category': category,
            'limit': countPerPage,
            'ORDER_BY': ORDER_BY,
            'OFFSET': OFFSET,
        }
        '''
        %(ORDER_BY)s
        LIMIT '%(limit)s'
        %(OFFSET)s
        '''

        print items_sql

        #TODO: double order
        sql = """
            SELECT p.id, p.name, p.slug, p.description, p.cost, p.weight,
                   p.buy_url, p.shop_name, p.shop_id, p.shop_url,
                   i.src as image_src
            FROM
                (
                    SELECT p.id, p.name, p.slug, p.description, p.cost, p.weight,
                           p.buy_url,
                           s.name as shop_name, s.id as shop_id, s.url as shop_url
                    FROM (%(ITEMS_SQL)s) as p

                    INNER JOIN %(shop_table)s as s
                    ON p.shop_id = s.id
                ) as p
            INNER JOIN
                (
                    SELECT DISTINCT ON (i.product_id) i.src, i.product_id
                    FROM %(image_table)s as i
                ) as i
            ON i.product_id = p.id
            %(ORDER_BY)s

        """ % {
            'image_table': 'product_image',
            'shop_table': 'shop_shop',
            'ITEMS_SQL': items_sql,
            'ORDER_BY': ORDER_BY,
        }

        return self.raw(sql)
