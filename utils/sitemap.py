# *- coding: utf-8 -*-
from datetime import datetime
import django
import math
from urlparse import urljoin
import xml.etree.ElementTree as ET

from goldpoisk.templates import get_menu
from goldpoisk.product.models import Product

host = 'http://goldpoisk.ru/'
NOW = datetime.now().isoformat()

def generate_sitemap():
    global root
    xml = ET.ElementTree(ET.Element('urlset', {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'
    }))
    root = xml.getroot()

    append_node('/', NOW, 0.7)
    append_node('/best', NOW, 0.7)
    generate_category_sitemap()
    generate_items_sitemap()

    f = open('sitemap.xml', 'w')
    xml.write(f, encoding='utf8', xml_declaration=True)

def generate_category_sitemap():
    countPerPage = 30

    for category in get_menu():
        append_node(category['href'], NOW, 0.5)
        products, count = Product.get_by_category(category['href'], 1, countPerPage)
        totalPages = int(math.ceil(float(count) / countPerPage)) or 1
        print "%s: %d pages" % (category['href'], totalPages)
        for i in range(2, totalPages + 1):
            path = urljoin(category['href'], '?page=%d' % i)
            append_node(path, NOW, 0.4)

def generate_items_sitemap():
    for product in Product.objects.filter(item__isnull=False):
        append_node(product.get_absolute_url(), NOW, 0.6)

def append_node(path, lastmod, priority):
    global root
    node = ET.Element('url')
    loc = ET.SubElement(node, 'loc')
    loc.text = urljoin(host, path)

    lastmod_node = ET.SubElement(node, 'lastmod')
    lastmod_node.text = lastmod

    priority_node = ET.SubElement(node, 'priority')
    priority_node.text = str(priority)
    root.append(node)

if __name__ == '__main__':
    django.setup()
    generate_sitemap()
