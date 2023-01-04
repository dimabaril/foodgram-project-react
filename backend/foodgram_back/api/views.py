from django.shortcuts import render

from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from djoser.views import UserViewSet
# поиск # фильтр
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from recipes.models import (
    Tag, Ingredient, Recipe, Subscription,
    Favorite, ShoppingCart, Recipe_Ingredients)
from users.models import (User, )
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    SubscriptionSerializer, ShortRecipeSerializer)
from .pagination import Page6PageNumberPagination
from .filters import RecipeFilter

from django.http import HttpResponse
#from reportlab.pdfbase import pdfmetrics
#from reportlab.pdfbase.ttfonts import TTFont
#from reportlab.pdfgen import canvas


class CustomUserViewSet(UserViewSet):  # UserViewSet так только админу список даёт
    pagination_class = Page6PageNumberPagination

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    @action(detail=True, methods=['post', 'delete', ])
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if user == author:
                return Response({
                    'errors': 'Вы не можете подписываться на себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            if Subscription.objects.filter(user=user, author=author).exists():
                return Response({
                    'errors': 'Вы уже подписаны на данного пользователя'
                }, status=status.HTTP_400_BAD_REQUEST)
            subscription = Subscription.objects.create(
                user=user, author=author)
            serializer = SubscriptionSerializer(subscription, )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if request.method == 'DELETE':
        subscription = Subscription.objects.filter(user=user, author=author)
        if subscription:
            subscription.delete()
            return Response(
                'successfully deleted', status=status.HTTP_204_NO_CONTENT)
        return Response({
                "errors": "Ошибка удаления, вы не подписаны"
                }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', ])
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        pages = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = Page6PageNumberPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    #filter_backends = (
    #    DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    #filterset_fields = ('author', )
    # search_fields = ('name', 'author__username')
    # ordering_fields = ('name', 'pub_date')  # если не прописать то все поля
    # ordering = ('id',) # можно прописать сортировку

    @action(detail=True, methods=['post', 'delete', ])
    def favorite(self, request, pk):
        if request.method == 'POST':
            favorite, get_status = Favorite.objects.get_or_create(
                recipe_id=pk, user=request.user)
            if get_status:
                # serializer = AddFavoriteShoppingCartSerializer(favorite)
                serializer = ShortRecipeSerializer(Recipe.objects.get(id=pk))
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response({
                "errors": "Ошибка добавления, рецепт уже в избранном"
                }, status=status.HTTP_400_BAD_REQUEST)
        # if request.method == 'DELETE':
        favorite = Favorite.objects.filter(recipe_id=pk, user=request.user)
        if favorite:
            favorite.delete()
            return Response(
                'successfully deleted', status=status.HTTP_204_NO_CONTENT)
        return Response({
                "errors": "Ошибка удаления, рецепта нету в избранном"
                }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            shoppingcart, get_status = ShoppingCart.objects.get_or_create(
                recipe_id=pk, user=request.user)
            if get_status:
                # serializer = AddFavoriteShoppingCartSerializer(shoppingcart)
                serializer = ShortRecipeSerializer(Recipe.objects.get(id=pk))
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response({
                "errors": "Ошибка добавления, рецепт уже в списке покупок"
                }, status=status.HTTP_400_BAD_REQUEST)
        # if request.method == 'DELETE':
        shoppingcart = ShoppingCart.objects.filter(
            recipe_id=pk, user=request.user)
        if shoppingcart:
            shoppingcart.delete()
            return Response(
                'successfully deleted', status=status.HTTP_204_NO_CONTENT)
        return Response({
                "errors": "Ошибка удаления, рецепта нету в списке покупок"
                }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, )
    def download_shopping_cart(self, request):
        final_dict = {}
        ingredients = Recipe_Ingredients.objects.filter(
            recipe__shoppingcarts__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        #print(ingredients)
        for item in ingredients:
            name = item[0]
            if name not in final_dict:
                final_dict[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_dict[name]['amount'] += item[2]
        content = ''
        for i, (name, data) in enumerate(final_dict.items(), 1):
            content += (f'{i} {name} - {data["amount"]}, '
                        f'{data["measurement_unit"]}''\n')
        response = HttpResponse(content, content_type='application/txt')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.txt"')
        return response


#class Recipe_IngredientsViewSet(viewsets.ModelViewSet):
#    queryset = Recipe_Ingredients.objects.all()
#    serializer_class = Recipe_IngredientsSerializer
#
#
#class SubscriptionViewSet(viewsets.ModelViewSet):
#    queryset = Subscription.objects.all()
#    serializer_class = SubscriptionSerializer
