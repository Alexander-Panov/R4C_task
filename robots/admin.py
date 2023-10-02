from django.contrib import admin

from robots.models import Robot


class RobotAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Model info", {"fields": ["serial", "model", "version"]}),
        ("Date info", {"fields": ["created"]})
    ]
    list_display = ["serial", "created"]
    list_filter = ["created"]


# Register your models here.
admin.site.register(Robot, RobotAdmin)