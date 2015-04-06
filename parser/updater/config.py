import time

TYPES = {
    'rings': 1,
    'necklace': 3,
    'pendants': 5,
    'brooches': 7,
    'earrings': 6,
    'watches': 8
}

SHOPS = {
    'Sunlight': 6,
}

TYPE_KEY = 'earrings'
TYPE_SHOP = 'Sunlight'

TYPE_ID = TYPES[TYPE_KEY]
SHOP_ID = SHOPS[TYPE_SHOP]
print '-'*100
print 'TYPE', TYPE_KEY, TYPE_ID
print '-'*100
print 'SHOP', TYPE_SHOP, SHOP_ID
print '-'*100
time.sleep(5)
