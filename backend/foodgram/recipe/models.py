from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .validators import color_validator

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=7, validators=[color_validator])
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Tag'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Inredient')
    measurement_unit = models.CharField(max_length=20,
                                        verbose_name='Measurement unit')

    class Meta:
        verbose_name = 'Ingredient'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]

    def __str__(self):
        return self.name


class Recipes(models.Model):
    tags = models.ManyToManyField(Tag, related_name='tags')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Author')

    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientPerRecipe',
        verbose_name='Ingredients',
        related_name='recipes',
    )
    is_favorited = models.ManyToManyField(
        User, related_name='favorite', blank=True, default=False)
    is_in_shopping_cart = models.ManyToManyField(
        User, related_name='shopping_cart', blank=True, default=False)
    name = models.CharField(max_length=200,
                            verbose_name='Recipe title')
    image = models.ImageField(upload_to='recipe/images/', null=True, blank=True)
    text = models.TextField(blank=False, default='default text')
    cooking_time = models.FloatField(default='100')
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Recipe'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngredientPerRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ingredient',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Recipe',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Amount',
    )

    class Meta:

        verbose_name = 'Ingredient amount'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique ingredients recipe')
        ]

    def __str__(self):
        return str(self.recipe)
