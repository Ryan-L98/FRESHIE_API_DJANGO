from django.contrib.auth.models import User
from django.db.models import fields
from django.db.models.lookups import Lookup
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, ReadOnlyField
from . import models

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Recipe
        fields = '__all__'

class favouriteMealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.favouriteMeals
        fields = '__all__'
        depth = 1

class CalorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Calories
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class consumedMealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.consumedMeals
        fields = '__all__'
        depth = 1