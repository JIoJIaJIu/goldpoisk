import time

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
