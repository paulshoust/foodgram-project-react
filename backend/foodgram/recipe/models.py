from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .validators import color_validator

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='Тэг')
    color = models.CharField(max_length=7, validators=[color_validator],
                             verbose_name='Цвет')
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Ингредиент')
    measurement_unit = models.CharField(max_length=20,
                                        verbose_name='Ед.измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]
        ordering = ['-id']

    def __str__(self):
        return self.name


class Recipes(models.Model):
    tags = models.ManyToManyField(Tag, related_name='tags', verbose_name='Тэг')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')

    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientPerRecipe',
        verbose_name='Ингредиент',
        related_name='recipes',
    )
    is_favorited = models.ManyToManyField(
        User, related_name='favorite', blank=True,
        verbose_name='Избранное')
    is_in_shopping_cart = models.ManyToManyField(
        User, related_name='shopping_cart', blank=True,
        verbose_name='Корзина')
    name = models.CharField(max_length=200,
                            verbose_name='Рецепт')
    image = models.ImageField(upload_to='recipe/images/', null=True,
                              blank=True, verbose_name='Фото')
    text = models.TextField(blank=False, default='default text',
                            verbose_name='Инструкции')
    cooking_time = models.PositiveSmallIntegerField(verbose_name='Время')
    pub_date = models.DateTimeField(default=timezone.now,
                                    verbose_name='Дата создания')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngredientPerRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Вес/объем',
    )

    class Meta:

        verbose_name = 'Объем/вес ингредиентов'
        verbose_name_plural = 'Объем/вес ингредиентов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique ingredients recipe')
        ]
        ordering = ['-id']

    def __str__(self):
        return str(self.recipe)
