from django.contrib.auth.models import User
from django.core import exceptions
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import fields
from django.db.models.lookups import Lookup
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, ReadOnlyField
from rest_auth.registration.serializers import RegisterSerializer
from . import models

class recipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Recipe
        fields = '__all__'

class favouriteMealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.favouriteMeals
        fields = '__all__'
        depth = 1

class clientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = '__all__'
        depth = 1

class personalTrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonalTrainer
        fields = '__all__'
        depth = 1

class registerSerializer(RegisterSerializer):
    firstName = serializers.CharField(write_only=True)
    lastName = serializers.CharField(write_only=True)
    isPersonalTrainer = serializers.BooleanField(write_only=True)
    referralCode = serializers.CharField(write_only=True)
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }
    def custom_signup(self, request, user):
        user.isPersonalTrainer = self.validated_data.get('isPersonalTrainer')
        user.first_name = self.validated_data.get('firstName')
        user.last_name = self.validated_data.get('lastName')
        user.save()
        if user.isPersonalTrainer :
            personalTrainer = models.PersonalTrainer(username= user.username, referralCode= user.username.upper() + str(user.id), user= user)
            personalTrainer.save()
        else:
            ref = self.validated_data.get('referralCode')
            if ref == None:
                client = models.Client(username= user.username, user= user)
            else:
                personalTrainer = models.PersonalTrainer.objects.get(referralCode=ref)
                client = models.Client(username= user.username, user= user, personalTrainer= personalTrainer)
            client.save()
            clientCalories = models.Client(client= client)
            clientCalories.save()

class mealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mealPlan
        fields = '__all__'
        depth = 1

class calorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Calories
        fields = '__all__'

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

class consumedMealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.consumedMeals
        fields = '__all__'