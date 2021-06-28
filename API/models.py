from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from rest_auth.models import TokenModel
from rest_framework import serializers

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    calories = models.IntegerField()
    servings = models.IntegerField(default=1, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, to_field='username', editable=False, null=True, related_name='recipes')
    custom = models.BooleanField(blank=True, null= True, default=None)

class mealPlan(models.Model):
    title = models.CharField(max_length=100)
    meal = models.ManyToManyField(Recipe, related_name='meals', blank=True)

class User(AbstractUser):
    isPersonalTrainer = models.BooleanField(null=True)
    mealPlans = models.ManyToManyField(mealPlan, related_name="user")

class PersonalTrainer(models.Model):
    username = models.CharField(max_length=20, unique=True)
    referralCode = models.CharField(max_length=10)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE, null=True, to_field="username", related_name= 'personalTrainer')

class Client(models.Model):
    username = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE, null=True, to_field="username", related_name= 'client')
    personalTrainer = models.ForeignKey(PersonalTrainer, on_delete=PROTECT, null=True, to_field='username', related_name='client')

class Calories(models.Model):
    dailyCalories = models.IntegerField(default=2250, null=False)
    currentCalories = models.IntegerField(default=0, null=False)
    client = models.OneToOneField(Client, on_delete=CASCADE, null=False, to_field='username', related_name='calories')

class consumedMeals(models.Model):
    meal = models.ForeignKey(Recipe, on_delete=CASCADE)
    client = models.ForeignKey(Client, on_delete=CASCADE, to_field='username', related_name='consumedMeals')
    mealType = models.CharField(max_length=15, blank=True)
    date = models.DateField(blank=True, auto_now_add=True)
    calories = models.IntegerField(default=323, null=False)

class favouriteMeals(models.Model):
    meal = models.ForeignKey(Recipe, on_delete=CASCADE)
    client = models.ForeignKey(Client, on_delete=CASCADE, to_field='username', related_name='favouriteMeals')


class CustomTokenSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()
    class Meta:
        model = TokenModel
        fields = ('key', 'user',)
        depth = 1