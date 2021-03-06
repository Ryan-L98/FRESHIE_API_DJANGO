from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('<username>/weekly-calories/', csrf_exempt(views.getWeeklyCalories), name= 'weekly-Calories'),
    path('recipes/<variant>/', csrf_exempt(views.recipeList), name='recipe-list-variant'),
    path('recipes/', csrf_exempt(views.addRecipe), name='recipe-list'),
    path('recipes/edit/<pk>/', csrf_exempt(views.editDelRecipe), name='recipe-details'),
    path('<username>/calories/', csrf_exempt(views.calorieView.as_view()), name='calories'),
    path('<username>/consumed-meals/', csrf_exempt(views.getConsumedMealsOn), name='consumed-meals'),
    path('<username>/add-consumed-meal/', csrf_exempt(views.addConsumedMeal), name='add-consumed-meal'),
    path('<username>/consumed-meal/<pk>/', csrf_exempt(views.getDelConsumedMeal), name='view-delete-meal'),
    path('<username>/fav-meals/', csrf_exempt(views.getFavMeals), name='fav-meals'),
    path('<username>/add-fav-meal/', csrf_exempt(views.addFavMeal), name='add-fav-meal'),
    path('<username>/fav-meal/<pk>/', csrf_exempt(views.getDelFavMeal), name='view-delete-fav-meal'),
    path('<username>/mealplans/', csrf_exempt(views.getMealPlans), name='mealplans'),
    path('<username>/add-mealplan/', csrf_exempt(views.addMealPlan), name='add-mealplan'),
    path('<username>/mealplan/<pk>/', csrf_exempt(views.getDelMealPlan), name='view-delete-mealplan'),
    path('<username>/', csrf_exempt(views.profileView), name='profile-page'),
    path('<username>/clients/', csrf_exempt(views.clientList), name= 'clients'),
    path('<username>/client/<clientName>/<action>/', csrf_exempt(views.clientProfile), name= 'client-profile'),
    path('<username>/add-personal-trainer/', csrf_exempt(views.addPersonalTrainer), name= 'add-personal-trainer'),
    path('<username>/restaurants/', csrf_exempt(views.getAddEditRestaurants), name='restaurants'),
    path('<username>/menu-items/', csrf_exempt(views.addEditDelMenuItem), name='menu-item'),

]
