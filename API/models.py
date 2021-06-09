from typing import DefaultDict
from django.db import models
from django.utils.timezone import now
from datetime import date
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import BLANK_CHOICE_DASH, IntegerField
from django.db.models.signals import post_save
from rest_auth.models import TokenModel
from django.dispatch import receiver
from rest_framework.fields import CurrentUserDefault
from rest_framework import serializers

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    calories = models.IntegerField()
    servings = models.IntegerField(default=1, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=SET_NULL, to_field='username', editable=False, null=True)

class Calories(models.Model):
    dailyCalories = models.IntegerField(default=2250, null=False)
    currentCalories = models.IntegerField(default=0, null=False)
    user = models.OneToOneField(User, on_delete=CASCADE, null=False, to_field='username')

class consumedMeals(models.Model):
    meal = models.ForeignKey(Recipe, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE, to_field='username')
    mealType = models.CharField(max_length=15, blank=True)
    date = models.DateField(blank=True, auto_now_add=True)

class favouriteMeals(models.Model):
    meal = models.ForeignKey(Recipe, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE, to_field='username')

@receiver(post_save, sender=User, dispatch_uid="assign calories to user")
def userCalorie(sender, instance, created, **kwargs):
    if created:
        user_calorie = Calories.objects.create(user=instance)
        user_calorie.save()

class CustomTokenSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()
    class Meta:
        model = TokenModel
        fields = ('key', 'user',)
        depth = 1