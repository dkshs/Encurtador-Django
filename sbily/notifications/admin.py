from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "user", "is_read", "created_at")
    list_filter = ("type", "user__username", "is_read", "created_at")
    search_fields = ("user__username", "title")
