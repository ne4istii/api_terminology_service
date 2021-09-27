from django.apps import apps
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Directory, Item, Version

User = get_user_model()

for app_config in apps.get_app_configs():
    for model in app_config.get_models():
        if admin.site.is_registered(model):
            admin.site.unregister(model)


class ItemInLine(admin.TabularInline):
    model = Version.items.through
    extra = 1
    min_num = 1
    verbose_name = 'Элемент справочника'
    verbose_name_plural = 'Элементы справочника'


class VersionInLine(admin.TabularInline):
    model = Version
    extra = 1
    min_num = 1
    verbose_name = 'Версия справочника'
    verbose_name_plural = 'Версии справочника'


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    inlines = (ItemInLine,)
    list_display = ('directory', 'name', 'pub_date')
    search_fields = ('name',)
    list_filter = ('pub_date',)
    ordering = ('-pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    inlines = (VersionInLine,)
    search_fields = ('uid', 'name')
    ordering = ('-uid',)
    empty_value_display = '-пусто-'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'value')
    search_fields = ('code', ' value')
    ordering = ('value',)
    empty_value_display = '-пусто-'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser')
        }),
    )
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    ordering = ('username', 'email')
    empty_value_display = '-пусто-'
