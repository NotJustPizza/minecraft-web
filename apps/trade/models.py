from django.db import models
from main.models import User

from django.core.validators import MaxValueValidator, MinValueValidator


class Deal(models.Model):
    seller = models.ForeignKey(
        User,
        models.PROTECT,
        related_name='sales',
        related_query_name='sale'
    )
    buyer = models.ForeignKey(
        User,
        models.PROTECT,
        related_name='purchases',
        related_query_name='purchase'
    )
    start_date = models.DateTimeField(auto_now_add=True, editable=False)
    end_date = models.DateTimeField(null=True, blank=True)
    aborted = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ['-start_date']


class DealItems(models.Model):
    deal = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='items',
        related_query_name='item'
    )
    item_id = models.PositiveSmallIntegerField()
    variation_id = models.PositiveSmallIntegerField()
    displayName = models.CharField(max_length=256)
    quantity = models.PositiveSmallIntegerField(validators=[MaxValueValidator(64)])
