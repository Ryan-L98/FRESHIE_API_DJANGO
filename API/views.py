from os import execlp
from django.contrib.auth.models import User
from django.core import exceptions
from django.db.models import query
from django.http import response
from django.utils import timezone, dateformat   
from django.db.models import fields, manager
from django.db.models.query import QuerySet
from django.http import request
from django.http.response import Http404, HttpResponse
from rest_auth.views import UserDetailsView
from datetime import date
from rest_framework import permissions
from rest_framework.fields import CurrentUserDefault
from API.models import Recipe
from django.shortcuts import render
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
    serializer_class = serializers.RecipeSerializer
    name = 'recipe-list'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#Recipe Details view
@method_decorator(csrf_exempt, name='dispatch')
class recipeDetails(generics.RetrieveUpdateDestroyAPIView, RecipeUserWritePermission):
    permission_classes = [RecipeUserWritePermission]
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    name = 'recipe-details'
#endregion

#region CALORIES
#Permissions
class CalorieUserWritePermission(BasePermission):
    message = 'Editing calories is restricted to assigned user only.'
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

#Calorie view
@method_decorator(csrf_exempt, name='dispatch')
class calorieView(generics.RetrieveUpdateAPIView, CalorieUserWritePermission):
    permission_classes = [CalorieUserWritePermission]
    queryset = models.Calories.objects.all()
    serializer_class = serializers.CalorieSerializer
    lookup_field = 'user'
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

class UserDetailsViewCustom(UserDetailsView):
    name = 'rest_user_details'
#endregion

#region consumedMeals view
class consumedMealsUserWritePermission(BasePermission):
    message = 'Editing consumed meals is restricted to assigned user only.'
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

@api_view(["GET"])
def getConsumedMealsToday(request, username):
    if request.user.username != username:
        return Response("INVALID USER", status=404)
    queryset = models.consumedMeals.objects.filter(user= request.user , date=timezone.now())
    len = queryset.count()
    if len == 0:
        return Response("You have not consumed any meals today!", status=204)
    serializer = serializers.consumedMealsSerializer(queryset, many=True)
    return Response(serializer.data, status=200)

@api_view(["GET","DELETE"])
def getDelConsumedMeal(request,username,pk):
    if request.user.username != username:
        return Response("INVALID USER", status=404)
    try:
        result = models.consumedMeals.objects.get(id=pk)
    except exceptions.ObjectDoesNotExist:
        return Response("Invalid recipe ID", status=404)
    if request.user != result.user:
        return Response("INVALID USER", status=404)
    serializer = serializers.consumedMealsSerializer(result)
    if request.method == "GET":
        return Response(serializer.data, status=200)
    if request.method == "DELETE":
        result.delete()
        return Response("Meal has been deleted successfully!", status=200)
        

@api_view(["POST"])
def addConsumedMeal(request, username):
    if request.user.username != username:
        return Response("INVALID USER", status=404)
    try:
        newMeal = models.Recipe.objects.get(id=request.data["recipeID"])
    except exceptions.ObjectDoesNotExist:
        return Response("Invalid Recipe ID", status=404)
    result = models.consumedMeals(mealType=request.data["mealType"], meal=newMeal, user=request.user)
    result.save()
    serializer = serializers.consumedMealsSerializer(result)
    return Response(serializer.data, status=202)

#endregion

#region Favourite meals

@api_view(["GET"])
def getFavMeals(request, username):
    if request.user.username != username:
        return Response("INVALID USER", status=404)
    queryset = models.favouriteMeals.objects.filter(user= request.user)
    len = queryset.count()
    if len == 0:
        return Response("You have not added any favourties!", status=204)
    serializer = serializers.favouriteMealsSerializer(queryset, many=True)
    return Response(serializer.data, status=200)

@api_view(["GET","DELETE"])
def getDelFavMeal(request, username, pk):
    if request.user.username != username:
        return Response("INVALID USER", status=404) 
    try:
        result = models.favouriteMeals.objects.get(id=pk)
    except exceptions.ObjectDoesNotExist:
        return Response("Invalid recipe ID", status=204)
    if request.user != result.user:
        return Response("INVALID USER", status=404)
    serializer = serializers.consumedMealsSerializer(result)
    if request.method == "GET":
        return Response(serializer.data, status=200)
    if request.method == "DELETE":
        result.delete()
        return Response("Meal has been deleted successfully!", status=202)

@api_view(["POST"])
def addFaveMeal(request, username):
    if request.user.username != username:
        return Response("INVALID USER", status=404)
    try:
        favMeal = models.Recipe.objects.get(id=request.data["recipeID"])
    except exceptions.ObjectDoesNotExist:
        return Response("Invalid recipe ID", status=204)
    if models.favouriteMeals.objects.filter(meal=favMeal).exists():
        return Response("This meal is already in your favourites", status=200)
    result = models.favouriteMeals(meal=favMeal, user=request.user)
    result.save()
    serializer = serializers.favouriteMealsSerializer(result)
    return Response(serializer.data, status=201)

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
