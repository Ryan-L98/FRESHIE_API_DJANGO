from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from . import models
from rest_auth.models import TokenModel

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'isPersonalTrainer']

class clientSerializer(serializers.ModelSerializer):
    user = userSerializer(read_only=True)
    class Meta:
        model = models.Client
        fields = '__all__'
        depth = 1

class personalTrainerSerializer(serializers.ModelSerializer):
    user = userSerializer()
    class Meta:
        model = models.PersonalTrainer
        fields = '__all__'
        depth = 1

class recipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Recipe
        fields = ['id', 'title', 'ingredients', 'instructions', 'calories', 'author', 'custom']

class favouriteMealsSerializer(serializers.ModelSerializer):
    client = clientSerializer()
    class Meta:
        model = models.favouriteMeals
        fields = '__all__'
        depth = 1

class registerSerializer(RegisterSerializer):
    firstName = serializers.CharField(write_only=True)
    lastName = serializers.CharField(write_only=True)
    isPersonalTrainer = serializers.BooleanField(write_only=True)
    referralCode = serializers.CharField(write_only=True, required=False)
    calories = serializers.IntegerField(write_only=True, required=False)
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
            if ref == "none":
                client = models.Client(username= user.username, user= user)
            else:
                personalTrainer = models.PersonalTrainer.objects.get(referralCode=ref)
                client = models.Client(username= user.username, user= user, personalTrainer= personalTrainer)
            client.save()
            clientCalories = models.Calories(dailyCalories= self.validated_data.get('calories'), client= client)
            clientCalories.save()

class mealPlanSerializer(serializers.ModelSerializer):
    meal = recipeSerializer(many=True)
    class Meta:
        model = models.mealPlan
        fields = '__all__'
        depth = 1

class calorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Calories
        fields = '__all__'

class consumedMealsSerializer(serializers.ModelSerializer):
    meal = recipeSerializer()
    client = clientSerializer()
    class Meta:
        model = models.consumedMeals
        fields = '__all__'
        depth = 1

class CustomTokenSerializer(serializers.ModelSerializer):
    user = userSerializer()
    class Meta:
        model = TokenModel
        fields = ('key', 'user',)
        depth = 1

class menuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.menuItem
        fields = '__all__'

class restaurantSerializer(serializers.ModelSerializer):
    menuItem = menuItemSerializer(many=True)
    class Meta: 
        model = models.Restaurant
        fields = '__all__'
        depth = 1