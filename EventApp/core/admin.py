from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import WebHookMessage, User, Ticket


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['date_joined',]
    list_display = ['username', 'name', 'email', 'date_joined',]
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'name', 'email', 'phone_number',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'password',)}),
        (_('Personal Info'),
            {'fields': ('name',)
            }),
        (_('Permissions'),
            {'fields': (
                'is_staff', 'is_active', 'groups',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'name', 'email', 'password1', 'password2')
        }),
    )


@admin.register(WebHookMessage)
class WebHookMessageAdmin(admin.ModelAdmin):
    ordering = ['recieved_at',]
    list_display = ['recieved_at', 'id',]
    search_fields = ('payload',)
    list_filter = ('recieved_at',)


@admin.register(Ticket)
class WebHookMessageAdmin(admin.ModelAdmin):
    ordering = ['updated_at', 'created_at',]
    list_display = ['email', 'ticket_id', 'updated_at', 'type',]
    search_fields = ('email', 'mobile', 'ticket_id', 'event_id',
        'first_name', 'title', 'last_name',)
    list_filter = ('event_id', 'type', 'canceled', 'updated_at',)
