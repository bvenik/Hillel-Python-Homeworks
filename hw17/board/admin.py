from django.contrib import admin
from .models import Profile, Category, Ad, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin layout configuration for Category model management.
    """
    list_display = ('name', 'description')

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """
    Admin layout configuration for Ad model with filtering options.
    """
    list_display = ('title', 'price', 'is_active', 'category', 'user', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin layout configuration for handling User comments.
    """
    list_display = ('user', 'ad', 'created_at')

admin.site.register(Profile)