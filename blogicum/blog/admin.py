from django.contrib import admin

from .models import (
    Post, Category, Location, Comment
)

admin.site.empty_value_display = 'Не задано'


class BlogInLine(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (BlogInLine,)
    list_display = ('title',)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
    )
    list_editable = (
        'category',
        'is_published',
    )
    search_fields = ('title',)
    list_filter = (
        'category',
        'is_published',
    )
    list_display_links = ('title',)


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    extra = 0

    list_display = (
        'post',
        'author',
        'created_at',

    )
    list_filter = (
        'author',
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location)
admin.site.register(Comment, CommentAdmin)
