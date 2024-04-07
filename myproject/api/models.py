from random import random

from django.db import models


# Create your models here.


class User(models.Model):
    openid = models.CharField(max_length=40)
    user_name = models.CharField(max_length=10)
    user_gender = models.CharField(max_length=10)
    user_create_time = models.DateTimeField(auto_now_add=True)
    user_avatar_index = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Merchant(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=4, decimal_places=2)


class MerchantFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='merchant_favorites')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = (('user', 'merchant'))


class Dish(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    score = models.DecimalField(max_digits=4, decimal_places=2)
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dishes')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'merchant'))

class DishFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dish_favorites')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='favorited_by')