from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import BLANK_CHOICE_DASH, IntegerField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.fields import CurrentUserDefault

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    calories = models.IntegerField()
    servings = models.IntegerField(default=1, null=False, blank=False)
    favourite = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=PROTECT, to_field='username')

class Calories(models.Model):
    dailyCalories = models.IntegerField(default=2250, null=False)
    currentCalories = models.IntegerField(default=0, null=False)
    user = models.OneToOneField(User, on_delete=CASCADE, null=False, to_field='username')

class consumedMeals(models.Model):
    meal = models.ForeignKey(Recipe, on_delete=PROTECT)
    user = models.ForeignKey(User, on_delete=CASCADE, to_field='username')

@receiver(post_save, sender=User, dispatch_uid="assign calories to user")
def userCalorie(sender, instance, created, **kwargs):
    if created:
        user_calorie = Calories.objects.create(user=instance)
        user_calorie.save()

