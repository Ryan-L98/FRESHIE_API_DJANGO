from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('recipes/', csrf_exempt(views.recipeList.as_view()), name='recipe-list'),
    path('recipes/<pk>/', csrf_exempt(views.recipeDetails.as_view()), name='recipe-details'),
    path('<username>/calories/', csrf_exempt(views.calorieView.as_view()), name='calories'),
    path('<username>/consumed-meals/', csrf_exempt(views.getConsumedMealsToday), name='consumed-meals'),
    path('<username>/add-consumed-meals/', csrf_exempt(views.addConsumedMeal), name='add-consumed-meal'),
    path('<username>/consumed-meals/<pk>/', csrf_exempt(views.getDelConsumedMeal), name='view-delete-meal'),
    path('<username>/fav-meals/', csrf_exempt(views.getFavMeals), name='fav-meals'),
    path('<username>/add-fav-meals/', csrf_exempt(views.addFavMeal), name='add-fav-meals'),
    path('<username>/fav-meals/<pk>/', csrf_exempt(views.getDelFavMeal), name='view-delete-fav-meal'),
    path('<username>/mealplans/', csrf_exempt(views.getMealPlans), name='mealplans'),
    path('<username>/add-mealplan/', csrf_exempt(views.addMealPlan), name='add-mealplan'),
    path('<username>/mealplan/<pk>/', csrf_exempt(views.getDelMealPlan), name='view-delete-mealplan'),
    path('<username>/', csrf_exempt(views.profileView), name='profile-page')
]
