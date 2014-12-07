from django.db import models
from django.utils.translation import ugettext_lazy as _

class BestBid(models.Model):
    item = models.ForeignKey('product.Item')

    class Meta:
        verbose_name = _('Best Bid')
        verbose_name_plural = _('Best Bids')

    def __unicode__(self):
        return self.item.__unicode__()
