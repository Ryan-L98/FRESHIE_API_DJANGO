# Generated by Django 3.2.3 on 2021-07-14 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_auto_20210708_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.CharField(default='bob', max_length=20),
            preserve_default=False,
        ),
    ]
