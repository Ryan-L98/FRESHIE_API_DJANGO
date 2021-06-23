from os import execlp, stat
from django.contrib.auth.models import User
from django.core import exceptions
from django.db.models import query
from django.http import response
from django.utils import timezone, dateformat   
from django.db.models import fields, manager
from django.db.models.query import QuerySet
from django.http import request
from django.http.response import Http404, HttpResponse, StreamingHttpResponse
from rest_auth.views import UserDetailsView
from datetime import date
from rest_framework import permissions
from rest_framework.fields import CurrentUserDefault
from rest_framework.views import exception_handler
from API.models import Recipe, mealPlan
from django.shortcuts import redirect, render
from rest_framework import serializers, status
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from . import serializers
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views
from django.utils.decorators import method_decorator
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication
from rest_auth.registration.views import LoginView, RegisterView

#region RECIPES

#Permissions
class RecipeUserWritePermission(BasePermission):
    message = 'Editing recipe is restricted to the author only.'
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

#Recipe list view
#@method_decorator(csrf_exempt, name='dispatch')
class recipeList(generics.ListCreateAPIView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.recipeSerializer
    name = 'recipe-list'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#Recipe Details view
@method_decorator(csrf_exempt, name='dispatch')
class recipeDetails(generics.RetrieveUpdateDestroyAPIView, RecipeUserWritePermission):
    permission_classes = [RecipeUserWritePermission]
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.recipeSerializer
    name = 'recipe-details'
#endregion

#region CALORIES
#Permissions
class CalorieUserWritePermission(BasePermission):
    message = 'Editing calories is restricted to assigned user only.'
    def has_object_permission(self, request, view, obj):
        return obj.client.username == request.user.username

#Calorie view
@method_decorator(csrf_exempt, name='dispatch')
class calorieView(generics.RetrieveUpdateAPIView, CalorieUserWritePermission):
    permission_classes = [CalorieUserWritePermission]
    queryset = models.Calories.objects.all()
    serializer_class = serializers.calorieSerializer
    lookup_field = 'client'
    lookup_url_kwarg = 'username'
    name = 'calories'

#endregion

#region Overriden user views
@method_decorator(csrf_exempt, name='dispatch')
class LoginViewCustom(LoginView):
    authentication_classes = (TokenAuthentication,)
    name = 'rest_login'

@method_decorator(csrf_exempt, name='dispatch')
class RegistrationViewCustom(RegisterView):
    authentication_classes = (TokenAuthentication,)
    name = 'rest_register'
    def create(self, request, *args, **kwargs):
        ref = request.data["referralCode"]
        if ref == "none":
            response = super().create(request, *args, **kwargs)
            custom_data = {"Signed up": "No personal Trainer", "status": "ok"}
            response.data.update(custom_data)
            return response
        else:
            try:
                personalTrainer = models.PersonalTrainer.objects.get(referralCode= ref)
            except exceptions.ObjectDoesNotExist:
                return Response("INVALID REFERRAL CODE!", status=404)
            response = super().create(request, *args, **kwargs)
            custom_data = {"Signed up": "With personal Trainer", "status": "ok"}
            response.data.update(custom_data)
            return response 

class UserDetailsViewCustom(UserDetailsView):
    name = 'rest_user_details'
#endregion

#region consumedMeals view
class consumedMealsUserWritePermission(BasePermission):
    message = 'Editing consumed meals is restricted to assigned user only.'
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

@api_view(["GET"])
def profileView(request, username):
    #print(request.user.username)
    if request.user.username != username:
        return Response("INVALID USER", status=404) 
    if request.user.isPersonalTrainer:
        pt = request.user.personalTrainer
        serializer = serializers.personalTrainerSerializer(pt)
        return Response(serializer.data, status=200)
    else :
        client = request.user.client
        serializer = serializers.clientSerializer(client)
        return Response(serializer.data, status=200)

@api_view(["GET"])
def clientList(request, username):
    if request.user.username != username or not request.user.isPersonalTrainer:
        return Response("INVALID USER", status=404)
    personalTrainer = request.user.personalTrainer
    clients = personalTrainer.client.all()
    if clients.count() == 0:
        return Response("You do not have any clients!")
    serializer = serializers.clientSerializer(clients, many=True)
    return Response(serializer.data, status=200)

@api_view(["GET", "POST", "DELETE"])
def clientProfile(request, username, clientName, action):
    if request.user.username != username or not request.user.isPersonalTrainer:
        return Response("INVALID USER", status=404)
    personalTrainer = request.user.personalTrainer
    try:
        client = personalTrainer.client.all().get(username= clientName)
    except exceptions.ObjectDoesNotExist:
        return Response("You do not have a client named " + clientName + "!", status=204)
    if request.method == "GET":
        if action == "view":
            serializer = serializers.clientSerializer(client)
            return Response(serializer.data, status=200)
        if action == "meal-plans":
            mealplans = client.user.mealPlans.all()
            if mealplans.count() == 0:
                return Response(client.username + " does not have any meal plans!", status=200)
            serializer = serializers.mealPlanSerializer(mealplans, many=True)
            return Response(serializer.data, status=200)
    if request.method == "DELETE":
        if action == "remove":
            personalTrainer.client.remove(client)
            # client.personalTrainer.remove(personalTrainer)
            return Response("You have successfully removed " + clientName + " as your client.", status=200)
        if action == "remove-meal-plan":
            try:
               mealPlan = client.user.mealPlans.all().get(id=request.data["mealPlanID"])
            except exceptions.ObjectDoesNotExist:
                return Response("INVALID MEAL PLAN ID", status= 404)
            client.user.mealPlans.remove(mealPlan)
            return Response("Successfully removed " + mealPlan.title + " from " + client.username + "'s meal plans!", status=202)
    if request.method == "POST":
        if action == "assign-meal-plan":
            try: 
                mealPlan = request.user.mealPlans.all().get(id=request.data["mealPlanID"])
            except exceptions.ObjectDoesNotExist:
                return Response("INVALID MEAL PLAN ID", status= 404)
            client.user.mealPlans.add(mealPlan)
            return Response(mealPlan.title + " assigned to " + clientName + "!", status=200)
    return Response("Invalid method and action pair you provided: " + request.method + " and " + action + " is invalid.", status=404)

@api_view(["POST"])
def addPersonalTrainer(request, username):
    if request.user.username != username:
        return Response("INVALID USER", status=404)
    if request.user.isPersonalTrainer:
        return Response("You are a personal trainer?", status=204)
    if request.user.client.personalTrainer is not None:
        return Response("You already have a personal trainer!", status=200)
    ref = request.data["referralCode"]
    try:
        personalTrainer = models.PersonalTrainer.objects.get(referralCode= ref)
    except exceptions.ObjectDoesNotExist:
        return Response("The referall code does not exist!", status= 404)
    client = request.user.client
    client.personalTrainer = personalTrainer
    client.save()
    return Response(personalTrainer.username + " is now your personal trainer!", status=200)


@api_view(["GET"])
def getConsumedMealsOn(request, username):
    if request.user.username != username or request.user.isPersonalTrainer:
        return Response("INVALID USER", status=404)
    queryset = models.consumedMeals.objects.filter(client= request.user.client , date=request.data["date"])
    len = queryset.count()
    if len == 0:
        return Response("You did not consume any meals!", status=204)
    serializer = serializers.consumedMealsSerializer(queryset, many=True)
    return Response(serializer.data, status=200)
        
    

@api_view(["GET","DELETE"])
def getDelConsumedMeal(request,username,pk):
    if request.user.username != username or request.user.isPersonalTrainer:
        return Response("INVALID USER", status=404)
    try:
        result = models.consumedMeals.objects.get(id=pk)
    except exceptions.ObjectDoesNotExist:
        return Response("Invalid recipe ID", status=404)
    if request.user.username != result.client.username:
        return Response("INVALID USER", status=404)
    serializer = serializers.consumedMealsSerializer(result)
    if request.method == "GET":
        return Response(serializer.data, status=200)
    if request.method == "DELETE":
        result.delete()
        return Response("Meal has been deleted successfully!", status=202)
        

@api_view(["POST"])
def addConsumedMeal(request, username):
    if request.user.username != username or request.user.isPersonalTrainer:
        return Response("INVALID USER", status=404)
    try:
        newMeal = models.Recipe.objects.get(id=request.data["recipeID"])
    except exceptions.ObjectDoesNotExist:
        return Response("Invalid Recipe ID", status=404)
    result = models.consumedMeals(mealType=request.data["mealType"], meal=newMeal, calories= newMeal.calories, client=request.user.client)
    result.save()
    serializer = serializers.consumedMealsSerializer(result)
    return Response(serializer.data, status=202)

#endregion

#region Favourite meals

@api_view(["GET"])
def getFavMeals(request, username):
    if request.user.username != username or request.user.isPersonalTrainer:
        return Response("INVALID USER", status=404)
    queryset = models.favouriteMeals.objects.filter(client= request.user.client)
    len = queryset.count()
    if len == 0:
        return Response("You have not added any favourties!", status=204)
    serializer = serializers.favouriteMealsSerializer(queryset, many=True)
    return Response(serializer.data, status=200)

@api_view(["GET","DELETE"])
def getDelFavMeal(request, username, pk):
    if request.user.username != username or request.user.isPersonalTrainer:
        return Response("INVALID USER", status=404) 
    try:
        result = models.favouriteMeals.objects.get(id=pk)
    except exceptions.ObjectDoesNotExist:
        return Response("Invalid recipe ID", status=204)
    if request.user.username != result.client.username:
        return Response("INVALID USER", status=404)
    serializer = serializers.consumedMealsSerializer(result)
    if request.method == "GET":
        return Response(serializer.data, status=200)
    if request.method == "DELETE":
        result.delete()
        return Response("Meal has been deleted successfully!", status=202)

@api_view(["POST"])
def addFavMeal(request, username):
    if request.user.username != username:
        return Response("INVALID USER", status=404)
    try:
        favMeal = models.Recipe.objects.get(id=request.data["recipeID"])
    except exceptions.ObjectDoesNotExist:
        return Response("Invalid recipe ID", status=204)
    if models.favouriteMeals.objects.filter(meal=favMeal).exists():
        return Response("This meal is already in your favourites", status=200)
    result = models.favouriteMeals(meal=favMeal, client=request.user.client)
    result.save()
    serializer = serializers.favouriteMealsSerializer(result)
    return Response(serializer.data, status=201)

@api_view(["GET"])
def getMealPlans(request, username):
    if request.user.username != username:
        return Response("INVALID USER", status=404)
    mealPlans = request.user.mealPlans
    if mealPlans.count() == 0:
        return Response("You do not have any meal plans!", status=204)
    serializer = serializers.mealPlanSerializer(mealPlans, many=True)
    return Response(serializer.data, status=201)


@api_view(["POST"])
def addMealPlan(request, username):
    if request.user.username != username:
        return Response("INVALID USER", status=404)
    mealsID = request.data["meals"]
    meals = models.Recipe.objects.filter(id__in= mealsID)
    if meals.count() == 0:
        return Response("NO RECIPES FOUND!", status=204)
    mealPlan = models.mealPlan(title= request.data["title"])
    mealPlan.save()
    for meal in meals:
        curr = meal
        curr.pk = None
        curr.save()
        mealPlan.meal.add(curr)
    request.user.mealPlans.add(mealPlan)
    serializer = serializers.mealPlanSerializer(mealPlan)
    return Response(serializer.data, status=201)

@api_view(["GET","POST", "DELETE"])
def getDelMealPlan(request, username, pk):
    if request.user.username != username:
        return Response("INVALID USER", status=404)
    try:
        mealPlan = models.mealPlan.objects.get(id=pk)
    except exceptions.ObjectDoesNotExist:
        return Response("Invalid meal plan ID!", status=204)
    if request.method == "GET":
        serializer = serializers.mealPlanSerializer(mealPlan)
        return Response(serializer.data, status=200)
    if request.method == "POST":
        mealPlan.title = request.data["title"]
        mealsID = request.data["meals"]
        meals = models.Recipe.objects.filter(id__in= mealsID)
        if meals.count() == 0:
            return Response("NO RECIPES FOUND!", status=204)
        curr = mealPlan.meal.all()
        mealPlan.meal.remove(*curr)
        mealPlan.meal.add(*meals)
        mealPlan.save()
        serializer = serializers.mealPlanSerializer(mealPlan)
        return Response(serializer.data, status=201)
    if request.method == "DELETE":
        mealPlan.delete()
        return Response("Meal plan has been deleted successfully!", status=202)

#region API urls
class index(generics.GenericAPIView):
    name = 'index'
    def get(self, request, *args, **kawrgs):
        return Response({
            'links below': "Do not require login to view :",
            'login' : reverse(LoginViewCustom.name, request=request),
            'register' : reverse(RegistrationViewCustom.name, request=request),
            'recipelist' : reverse(recipeList.name, request=request),
            'recipe details' : '/api/recipes/<pk>',
            '' : '',
            'links at da bottom' : 'Require login to view', 
            'user view' : reverse(UserDetailsViewCustom.name, request=request), 
            'calories' : '/api/<username>/calories/',
            'consumed meals' : '/api/<username>/consumed-meals/  <-- add id for details/delete view',
            'add consumed meals' : '/api/<username>/add-consumed-meals/',
            'favourite meals' : '/api/<username>/fav-meals/  <-- add id for details/delete view',
            'add favourite meals' : '/api/<username>/add-fav-meals/'
        }) 
#endregion
