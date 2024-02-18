from django.contrib import admin
from django.utils.html import format_html

from blog.models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Не задано'


@admin.register(Category)
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


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)


@admin.register(Post)
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
        'image_icon',
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
    fieldsets = (
        (
            'Содержание публикации',
            {
                'fields': (
                    'title',
                    'text',
                )
            },
        ),
        (
            'Подробная информация',
            {
                'fields': (
                    'is_published',
                    'author',
                    'location',
                    'category',
                    'pub_date',
                    'image',
                )
            },
        ),
    )

    def image_icon(self, object):
        if object.image:
            return format_html(
                '<img src="{}" width="100" height="100">', object.image.url
            )

    image_icon.short_description = 'Изображение'


@admin.register(Comment)
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
