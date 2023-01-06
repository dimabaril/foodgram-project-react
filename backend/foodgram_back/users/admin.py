from django.contrib import admin
# from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',)
    list_filter = ('username', 'email',)  # фильтр выглядит странно лучше поиск
    search_fields = ('username', 'email',)

# admin.site.register(User)
