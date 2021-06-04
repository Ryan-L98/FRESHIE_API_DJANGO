from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('recipes', csrf_exempt(views.recipeList.as_view()), name='recipe-list'),
    path('recipes/<pk>/', csrf_exempt(views.recipeDetails.as_view()), name='recipe-details'),
    path('<username>/calories/', views.calorieView.as_view(), name='calories'),
    path('<username>/consumed-meals/', views.consumedMealsView.as_view(), name='consumed-meals'),
    path('<username>/consumed-meals/<pk>', views.consumedMealsDeleteView.as_view(), name='delete-meal')
]
