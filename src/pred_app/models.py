from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

def validate_decimals(value):
    try:
        return round(float(value), 2)
    except:
        raise ValidationError(
            _('%(value)s is not an integer or a float  number'),
            params={'value': value},
        )

class Portfolio(models.Model):
    balance = models.FloatField(null=False, validators = [

        MinValueValidator(0),
        validate_decimals


    ])
    user = models.OneToOneField(User, related_name="user_portfolio", on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_portfolio(sender, instance, created, **kwargs):
    if created:
        p_model = Portfolio.objects.create(balance=0, user=instance)
        p_model.save()


class holdings(models.Model):
    name = models.CharField(max_length=150, null=False)
    symbol = models.CharField(max_length=150, null=False)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, related_name="user_holdings", on_delete=models.CASCADE)

class Transaction(models.Model):
    name = models.CharField(max_length=150, null=False)
    symbol = models.CharField(max_length=150, null=False)
    quantity = models.IntegerField()
    type = models.CharField(max_length=150, null=False)
    price = models.FloatField()
    balance_before = models.FloatField()
    balance_after = models.FloatField()
    user = models.ForeignKey(User, related_name="user_transactions", on_delete=models.CASCADE)

class PopularStock(models.Model):
    name = models.CharField(max_length=150, null=False, unique=True)
    symbol = models.CharField(max_length=150, null=False, unique=True)
