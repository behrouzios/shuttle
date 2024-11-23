from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailTemplate, EmailLog


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'national_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'first_name', 'last_name', 'national_id', 'is_staff', 'is_active'),
        }),
    )


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_at', 'updated_at')
    search_fields = ('name', 'subject')
    ordering = ('-created_at',)


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("to_email", "template_name", "status", "sent_at")
    list_filter = ("status", "template_name", "sent_at")