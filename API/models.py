from django.conf import LazySettings, settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from rest_framework import serializers

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    calories = models.IntegerField()
    servings = models.IntegerField(default=1, null=True, blank=True)
    author = models.CharField(max_length=20, null=True)
    custom = models.BooleanField(blank=True, null= True, default=None)

class mealPlan(models.Model):
    title = models.CharField(max_length=100)
    meal = models.ManyToManyField(Recipe)

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

class Restaurant(models.Model): 
    name = models.CharField(max_length=20, blank=False)
    category = models.CharField(max_length=20, blank=False)
    address = models.CharField(max_length=100, blank=False)
    longitude = models.DecimalField(max_digits=11, decimal_places=7, blank=False)
    latitude = models.DecimalField(max_digits=11, decimal_places=7, blank=False)

class menuItem(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    calories = models.IntegerField(blank= False)
    restaurant = models.ForeignKey(Restaurant, on_delete=CASCADE, related_name='menuItem')


    
