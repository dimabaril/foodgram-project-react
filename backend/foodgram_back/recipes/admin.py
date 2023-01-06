from django.contrib import admin

from .models import (
    Tag, Ingredient, Recipe, Recipe_Ingredient, Subscription, Favorite,
    ShoppingCart, )


class Recipe_IngredientInline(admin.TabularInline):
    model = Recipe_Ingredient
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [Recipe_IngredientInline]
    list_display = ('id', 'name', 'author', 'favorites_count', )
    # фильтр выглядит странно лучше поиск
    list_filter = ('name', 'author__username', 'tags__name', )
    search_fields = ('name', 'author__username', 'tags__name', )

    def favorites_count(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )
    list_filter = ('name', )  # фильтр выглядит странно лучше поиск
    search_fields = ('name', )


admin.site.register(Tag)
admin.site.register(Subscription)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
