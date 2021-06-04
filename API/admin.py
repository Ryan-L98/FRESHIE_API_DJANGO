from django.contrib import admin
from . import models

admin.site.register(models.Recipe)
admin.site.register(models.Calories)
admin.site.register(models.consumedMeals)

