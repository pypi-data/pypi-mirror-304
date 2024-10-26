from django.contrib import admin
from . import models
from django.contrib.auth.models import User, Group


@admin.register(models.Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('media_id', 'name', 'category')
    list_filter = ('category',)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ('email', 'order_count')


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ('order_id', 'customer_id', 'name', 'date_ordered', 'category')
    list_filter = ('customer_id', 'date_ordered', 'category')


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date')
    list_filter = ('date',)


admin.site.unregister(User)
admin.site.unregister(Group)