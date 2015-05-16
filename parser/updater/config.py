#-*- coding: utf-8 -*-
LOG_LEVEL=10 #"DEBUG"

POSTGRES_DATABASE = 'dumps'
POSTGRES_USER = 'dev_goldpoisk'
POSTGRES_PASSWORD = 'dev12345'

def get_type(name):
    types = {
        "rings": [u"Кольца",],
        "bracelets": [u"Браслеты",],
        "necklace": [u"Ожерелья", u"Колье",],
        "chains": [u"Цепи", u"Цепочки"],
        "pendants": [u"Подвески",],
        "earrings": [u"Серьги",],
        "brooches": [u"Броши",],
        "watches": [u"Часы",],
    }

    for type_name in types:
        name = name.lower()
        for item in types[type_name]:
            if item.lower() == name:
                return TYPES[type_name]
    
    print "Unknown type: %s" % name
    raise Exception()

def get_shop_id(name):
    shop_id = SHOPS[name]
    if shop_id == None:
        print "Unknown shop: %s" % name
        raise Exception()

    return shop_id

TYPES = {
    'rings': 1,
    'bracelets': 2,
    'necklace': 3,
    'chains':4,
    'pendants': 5,
    'earrings': 6,
    'brooches': 7,
    'watches': 8,
}

SHOPS = {
    'gold585': 2,
    'Sunlight': 6,
}

'''
TYPE_KEY = 'bracelets'
TYPE_SHOP = 'gold585'

TYPE_ID = TYPES[TYPE_KEY]
SHOP_ID = SHOPS[TYPE_SHOP]
print '-'*100
print 'TYPE', TYPE_KEY, TYPE_ID
print '-'*100
print 'SHOP', TYPE_SHOP, SHOP_ID
print '-'*100
time.sleep(5)
'''
