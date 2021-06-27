# Generated by Django 3.2.3 on 2021-06-27 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_consumedmeals_calories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealplan',
            name='meal',
            field=models.ManyToManyField(blank=True, null=True, related_name='meals', to='API.Recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='custom',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
