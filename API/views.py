from django.contrib.auth.models import User
from django.db.models import fields
from django.db.models.query import QuerySet
from django.http import request
from django.http.response import Http404
from rest_auth.views import UserDetailsView
from rest_framework import permissions
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

@method_decorator(csrf_exempt, name='dispatch')
class consumedMealsView(generics.ListCreateAPIView, consumedMealsUserWritePermission):
    permission_classes = [consumedMealsUserWritePermission]
    queryset = models.consumedMeals.objects.all()
    serializer_class = serializers.consumedMealsSerializer
    lookup_field = 'user'
    lookup_url_kwarg = 'username'
    name = 'consumed-meals'

@method_decorator(csrf_exempt, name='dispatch')
class consumedMealsDeleteView(generics.RetrieveDestroyAPIView, consumedMealsUserWritePermission):
    permission_classes = [consumedMealsUserWritePermission]
    queryset = models.consumedMeals.objects.all()
    serializer_class = serializers.consumedMealsSerializer
    name = 'delete-meal'

#endregion

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
            'consumed meals' : '/api/<username>/consumed-meals/  <-- add id to end for delete view'
        }) 
#endregion
