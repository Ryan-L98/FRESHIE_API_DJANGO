from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from . import models

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Client)
admin.site.register(models.PersonalTrainer)
admin.site.register(models.mealPlan)
admin.site.register(models.Recipe)
admin.site.register(models.Calories)
admin.site.register(models.consumedMeals)

