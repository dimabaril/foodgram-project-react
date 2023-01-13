from django.db import models

from users.models import User

MODELS_STR_MAX_LENGTH = 10


class Tag(models.Model):
    """DB model for Tags."""
    name = models.CharField(
        verbose_name='Название',
        max_length=50,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        default='#ffffff',  # например, #49B64E
        unique=True,
    )
    slug = models.CharField(
        verbose_name='Slug',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:MODELS_STR_MAX_LENGTH]


class Ingredient(models.Model):
    """DB model for Ingredients."""
    name = models.CharField(
        verbose_name='Название',
        max_length=50,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=10,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredient with measurement_unit')
        ]

    def __str__(self):
        return self.name[:MODELS_STR_MAX_LENGTH]


class Recipe(models.Model):
    """DB model for Recipes."""
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=50,
        unique=True,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='uploads/',
    )
    text = models.TextField(
        verbose_name="Текстовое описание.",
        help_text="Текстовое описание.",
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        verbose_name='Ингредиент',
        related_name='recipes',
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.name[:MODELS_STR_MAX_LENGTH]


class RecipeIngredient(models.Model):
    """DB model for many to many relation for Ingredients In Recipe models."""
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique ingredient in recipe')
        ]


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptioner',
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptioning',
    )

    class Meta:
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique subscription')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique favorite')
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='shoppingcarts',
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcarts',
    )

    class Meta:
        verbose_name_plural = "Список покупок"
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique shoppingcart')
        ]
