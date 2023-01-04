# from django.contrib import admin
# from django.utils.html import format_html
from django.db import models
# потом юзера перекину/поправлю
# from django.contrib.auth import get_user_model
from users.models import User

MODELS_STR_MAX_LENGTH = 10

# User = get_user_model()


class Tag(models.Model):
    """DB model for Tags."""
    name = models.CharField(
        verbose_name='Название',
        max_length=50,
        #unique=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        default='#ffffff',  # например, #49B64E
        #unique=True,
        blank=True,
    )
    slug = models.CharField(
        verbose_name='Slug',
        max_length=50,
        #unique=True,
        blank=True,
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
        unique=True,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=10,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

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
        blank=True,  # после дебага удалить
    )
    text = models.TextField(
        verbose_name="Текстовое описание.",
        blank=True,  # после дебага удалить
        # help_text="Текстовое описание.",
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        verbose_name='Ингредиент',
        related_name='recipes',
        blank=True,  # после дебага удалить
        through='Recipe_Ingredients'
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name='Тег',
        related_name='recipes',
        blank=True,  # после дебага удалить
        through='Recipe_Taaags'  # можно без этого, неявно.
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        blank=True,  # после дебага удалить
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


class Recipe_Ingredients(models.Model):
    """DB model for many to many relation for Ingredients In Recipe models."""
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
    #    related_name='recipe_ingredients'  # можно, но не нужно
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class Recipe_Taaags(models.Model):
    # можно эту таблицу жестко не прописывать
    """DB model for many to many relation for Tags In Recipe models."""
    tag = models.ForeignKey(
        to=Tag,
        on_delete=models.CASCADE,
    #    related_name='recipe_tags'  # можно, но не нужно
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tags'
    )

    class Meta:
        verbose_name = 'Теги в рецепте'
        verbose_name_plural = 'Теги в рецептах'


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


class Favorite(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        # related_name='favorites',
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name_plural = "Избранное"


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
