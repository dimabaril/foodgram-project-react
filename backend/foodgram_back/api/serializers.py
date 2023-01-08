# from pprint import pprint
from django.shortcuts import get_object_or_404
from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserSerializer, UserCreateSerializer

from foodgram_back.settings import DJOSER

from recipes.models import (
    Tag, Ingredient, Recipe, Recipe_Ingredient, Subscription,
    Favorite, ShoppingCart, )
from users.models import (User, )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')
        read_only_fields = (DJOSER['LOGIN_FIELD'],)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password', )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class Recipe_IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Recipe_Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeSerializer(serializers.ModelSerializer):
    '''Some text.'''
    image = Base64ImageField()
    ingredients = Recipe_IngredientSerializer(
        source='recipe_ingredients', many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time', )

# Хотел сделать с валидеацией, через постман всё работает но через фронт просто не добавляются рецепты, и редактирование работает только если не менять ингредиенты
#    def validate(self, data):
#        ingredients = self.initial_data.get('ingredients')
#        if not ingredients:
#            raise serializers.ValidationError({
#                'ingredients': 'Добавьте ингредиент'})
#        ingredient_list = []
#        for ingredient_item in ingredients:
#            ingredient = get_object_or_404(Ingredient,
#                                           id=ingredient_item['id'])
#            if not ingredient:
#                raise serializers.ValidationError(
#                    'Ингредиент отсутствует в базе')
#            if ingredient in ingredient_list:
#                raise serializers.ValidationError({
#                    'ingredients': 'Ингредиенты не должны повторяться'})
#            ingredient_list.append(ingredient)
#            if not isinstance(ingredient_item['amount'], int):
#                raise serializers.ValidationError({
#                    'ingredients': ('Количство должно быть числовым значением')
#                })
#            if int(ingredient_item['amount']) < 0:
#                raise serializers.ValidationError({
#                    'ingredients': ('Убедитесь, что значение количества '
#                                    'ингредиента больше 0')
#                })
#        data['ingredients'] = ingredients
#        tags = self.initial_data.get('tags')
#        if not tags:
#            raise serializers.ValidationError({
#                'tags': 'Добавьте теги'})
#        for tag_id in tags:
#            if not Tag.objects.filter(id=tag_id).exists():
#                raise serializers.ValidationError({
#                    'tags': 'Тег отсутствует в базе'
#                })
#        data['tags'] = tags
#        return data
#
#    def create(self, validated_data):
#        # pprint(self.initial_data)
#        # print()
#        # pprint(validated_data)
#        # print()
#        # без валидации можно достать из self.initial_data вместо validated_data
#        recipe_ingredients = validated_data.pop('ingredients')
#        tags = validated_data.pop('tags')
#        recipe = Recipe.objects.create(
#            **validated_data, author=self.context.get('request').user)
#        recipe.tags.set(tags)
#        for recipe_ingredient in recipe_ingredients:
#            Recipe_Ingredient.objects.create(
#                ingredient_id=recipe_ingredient.get('id'),
#                recipe=recipe,
#                amount=recipe_ingredient.get('amount'))
#        return recipe
#
#    def update(self, instance, validated_data):
#        instance.image = validated_data.get('image', instance.image)
#        instance.name = validated_data.get('name', instance.name)
#        instance.text = validated_data.get('text', instance.text)
#        instance.cooking_time = validated_data.get(
#            'cooking_time', instance.cooking_time
#        )
#        instance.tags.clear()
#        tags = validated_data.get('tags')
#        instance.tags.set(tags)
#        recipe_ingredients = validated_data.get('ingredients')
#        Recipe_Ingredient.objects.filter(recipe=instance).delete()
#        if recipe_ingredients:
#            for ingredient in recipe_ingredients:
#                Recipe_Ingredient.objects.create(
#                    recipe=instance,
#                    ingredient_id=ingredient.get('id'),
#                    amount=ingredient.get('amount'),
#                )
#        instance.save()
#        return instance

    def create(self, validated_data):
        # pprint(self.initial_data)
        recipe_ingredients = self.initial_data.pop('ingredients')
        tags = self.initial_data.pop('tags')
        recipe = Recipe.objects.create(
            **validated_data, author=self.context.get('request').user)
        recipe.tags.set(tags)
        for recipe_ingredient in recipe_ingredients:
            Recipe_Ingredient.objects.create(
                ingredient_id=recipe_ingredient.get('id'),
                recipe=recipe,
                amount=recipe_ingredient.get('amount'))
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags = self.initial_data.get('tags')
        instance.tags.set(tags)
        recipe_ingredients = self.initial_data.get('ingredients')
        Recipe_Ingredient.objects.filter(recipe=instance).delete()
        if recipe_ingredients:
            for ingredient in recipe_ingredients:
                Recipe_Ingredient.objects.create(
                    recipe=instance,
                    ingredient_id=ingredient.get('id'),
                    amount=ingredient.get('amount'),
                )
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    '''Some text.'''
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count')

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=obj.user, author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.author)
        if limit:
            recipes = recipes[:int(limit)]
        return ShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


#class AddFavoriteShoppingCartSerializer(serializers.ModelSerializer):
#    # Этот сериалайзер замьютил, наверное можно выпилить
#    id = serializers.IntegerField(source='recipe.id')
#    name = serializers.CharField(source='recipe.name')
#    image = Base64ImageField(source='recipe.image')
#    cooking_time = serializers.CharField(source='recipe.cooking_time')
#
#    class Meta:
#        model = Favorite
#        fields = ('id', 'name', 'image', 'cooking_time', )


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )
