from django.contrib import admin
from .models import User, Habit, Tracker, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Habit)
admin.site.register(Tracker)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'habit', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)