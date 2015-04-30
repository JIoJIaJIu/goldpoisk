from django.db import models

from goldpoisk.settings import UPLOAD_TO
from goldpoisk.product.models import Item

class Banner(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to=UPLOAD_TO['promotion'])
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        return self.image.url

class Promotion(models.Model):
    banner = models.ForeignKey(Banner)
    x = models.DecimalField(decimal_places=2, max_digits=5)
    y = models.DecimalField(decimal_places=2, max_digits=5)
    item = models.ForeignKey(Item)
