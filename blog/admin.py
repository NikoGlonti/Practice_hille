from django.contrib import admin

from .models import Comment, Post


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'brief_description', 'full_description', 'posted']
    list_filter = ['author']
    search_fields = ['title']
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'text', 'post', 'posted_com']
    list_filter = ['username']
    search_fields = ['username']
    ordering = ['posted_com', 'post']
