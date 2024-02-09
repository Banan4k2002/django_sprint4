from django.contrib import admin

from .models import Category, Location, Post, Comment


admin.site.empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at',
    )
    list_editable = (
        'author',
        'location',
        'category',
        'is_published',
    )
    search_fields = ('title',)
    list_filter = (
        'is_published',
        'pub_date',
        'author',
        'location',
        'category',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'created_at',
        'author',
        'post',
    )
    list_editable = (
        'author',
        'post',
    )
    search_fields = ('text',)
    list_filter = (
        'created_at',
        'author',
        'post',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
