from django.db import models
from alljewel.settings import UPLOAD_TO

# Create your models here.
class Product(models.Model):
    type = models.ForeignKey('Type')
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return '%s "%s"' % (self.type.name, self.name);

class Item(models.Model):
    cost = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()
    product = models.ForeignKey('Product', related_name='items')
    is_new = models.BooleanField()
    sale = models.BooleanField()

    def __unicode__(self):
        return '%s: %d' % (self.product.__unicode__(), self.cost)


class Type(models.Model):
    name = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Gem(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to=UPLOAD_TO['gem'], null=True)

    def __unicode__(self):
        return self.name

class Image(models.Model):
    src = models.ImageField(upload_to=UPLOAD_TO['product'])
    product = models.ForeignKey(Product, related_name="images")
