#-*- coding: utf8 -*-
import re

def map_row(row):
    #TODO:
    weight_reg = re.compile(r'\d+(\.\d+)?')
    weight = 0
    '''
    if weight_reg.search(row.weight):
        weight = decimal.Decimal(weight_reg.search(row.weight).group(0))
    '''

    return {
        'name': row.name,
        'number': row.article,
        'type': row.category,
        'price': row.price,
        'url': row.url,
        'count': row.count,
        #'material': row.material or '',
        #'weight': weight,
        'description': row.description
    }

class Row(object):
    def __init__(self, row, keys):
        self.row = row
        self.keys = keys

    def __getattr__(self, key):
        i = self.keys.index(key)
        data = self.row[i]
        if key == 'name' and data:
            data = data.replace(u'тов', '').strip()

        if type(data) == "string":
            return data.decode("utf-8")
        return data

    def __str__(self):
        return dict([(key, self.__getattr__(key)) for key in self.keys]).__str__()

def convert(description, rows):
    d = []
    collumns = [q[0].decode('utf-8') for q in description]

    for row in rows:
        d.append(Row(row, collumns))
    return d
