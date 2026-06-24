from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ProjectTask


class ProjectTaskInline(admin.TabularInline):
    model = ProjectTask
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [ProjectTaskInline]

    list_display = ('username', 'email', 'phone_number', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('About', {'fields': ('phone_number',)}),
    )


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status_code', 'created_at')

    list_filter = ('status_code', 'created_at')

    search_fields = ('title', 'user__username')

    actions = ['mark_as_urgent']

    @admin.action(description='Make urgent')
    def mark_as_urgent(self, request, queryset):
        updated_count = queryset.update(status_code='URGENT')
        self.message_user(request, f"{updated_count} tasks were marked as urgent.")
