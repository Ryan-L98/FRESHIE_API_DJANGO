from django.urls import path, include
from . import views

urlpatterns = [
    path('recipes', views.recipeList.as_view(), name='recipe-list'),
    path('recipes/<pk>/', views.recipeDetails.as_view(), name='recipe-details'),
    path('<username>/calories/', views.calorieView.as_view(), name='calories'),
    #path('signup', views.userCreate.as_view(), name='signup'),

]
