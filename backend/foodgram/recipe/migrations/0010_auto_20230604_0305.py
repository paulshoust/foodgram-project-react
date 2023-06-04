# Generated by Django 3.2.19 on 2023-06-04 00:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0009_auto_20230529_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='is_favorited',
            field=models.ManyToManyField(blank=True, related_name='favorite', to=settings.AUTH_USER_MODEL, verbose_name='Избранное'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='is_in_shopping_cart',
            field=models.ManyToManyField(blank=True, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='Корзина'),
        ),
    ]
