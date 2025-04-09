from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Topic, Entry, Like, Dislike, Comment, Notification

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner', 'date_added', 'is_private', 'like_count', 'dislike_count', 'comment_count')
    list_filter = ('is_private', 'date_added')
    search_fields = ('text', 'owner__username')
    raw_id_fields = ('owner',)
    date_hierarchy = 'date_added'

    def like_count(self, obj):
        return obj.like_set.count()

    like_count.short_description = 'Likes'

    def dislike_count(self, obj):
        return obj.dislike_set.count()

    dislike_count.short_description = 'Dislikes'

    def comment_count(self, obj):
        return obj.comment_set.count()

    comment_count.short_description = 'Comments'


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('topic', 'truncated_text', 'date_added')
    list_filter = ('date_added', 'topic')
    search_fields = ('text', 'topic__text')

    def truncated_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    truncated_text.short_description = 'Text'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'topic__text')
    raw_id_fields = ('user', 'topic')


@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'topic__text')
    raw_id_fields = ('user', 'topic')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'truncated_text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username', 'topic__text')
    raw_id_fields = ('user', 'topic')

    def truncated_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    truncated_text.short_description = 'Text'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'topic', 'action', 'is_read', 'created_at')
    list_filter = ('is_read', 'action', 'created_at')
    search_fields = ('recipient__username', 'sender__username', 'topic__text')
    raw_id_fields = ('recipient', 'sender', 'topic')
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    mark_as_read.short_description = "Mark selected notifications as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

    mark_as_unread.short_description = "Mark selected notifications as unread"