from django.contrib import admin
# from django.utils.html import format_html

from .models import (
    Tag, Ingredient, Recipe, Recipe_Ingredients, Subscription, Favorite,
    ShoppingCart, )  # Recipe_Tags)


# admin.site.register(Tag)
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Recipe_Ingredients)
# admin.site.register(Recipe_Tags)
admin.site.register(Subscription)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
