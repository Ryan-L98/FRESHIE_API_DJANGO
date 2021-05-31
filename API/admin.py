from django.contrib import admin
from .models import Calories, Recipe

admin.site.register(Recipe)
admin.site.register(Calories)

