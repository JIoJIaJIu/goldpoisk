from django.test import TestCase
from product.models import Product, Item, Material, Gem, Type


class MaterialTest(TestCase):
    def test_create(self):
        material = Material(name='Gold')
        self.assertEqual(material.name, 'Gold')

class GemTest(TestCase):
    def test_create(self):
        material = Gem(name='Diamond')
        self.assertEqual(material.name, 'Diamond')

class ProductTest(TestCase):
    def test_create(self):
        materials = [
            {'name': 'Gold'},
            {'name': 'Silver'},
            {'name': 'Platinum'},
        ]

        gems = [
            {'name': '1'},
            {'name': '2'},
            {'name': '3'},
        ]

        product = Product(type=Type(1, name='Ring'), name='Ring XYZ')
        product.save()

        map(lambda m: product.materials.create(**m), materials);
        map(lambda g: product.gems.create(**g), gems);

        self.assertEqual(product.type.name, 'Ring')
        self.assertEqual(product.materials.all()[1].name, 'Silver')
        self.assertEqual(product.gems.all()[2].name, '3')
