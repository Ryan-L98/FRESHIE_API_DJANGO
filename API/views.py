from django.contrib.auth.models import User
from django.db.models import fields
from django.http import request
from django.http.response import Http404
from rest_framework import permissions
from API.models import Recipe
from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views
from django.utils.decorators import method_decorator
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication
from rest_auth.registration.views import LoginView

#region RECIPES

#Permissions
class RecipeUserWritePermission(BasePermission):
    message = 'Editing recipe is restricted to the author only.'
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

#Recipe list view
class recipeList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#Recipe Details view
class recipeDetails(generics.RetrieveUpdateDestroyAPIView, RecipeUserWritePermission):
    permission_classes = [RecipeUserWritePermission]
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
#endregion

#region CALORIES
#Permissions
class CalorieUserWritePermission(BasePermission):
    message = 'Editing calories is restricted to assigned user only.'
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

#Calorie view
class calorieView(generics.RetrieveUpdateAPIView, CalorieUserWritePermission):
    permission_classes = [CalorieUserWritePermission]
    queryset = models.Calories.objects.all()
    serializer_class = serializers.CalorieSerializer
    lookup_field = 'user'
    lookup_url_kwarg = 'username'

#endregion

# myapp.views.py

@method_decorator(csrf_exempt, name='dispatch')
class LoginViewCustom(LoginView):
    authentication_classes = (TokenAuthentication,)