from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'sk_python_project'
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('profile/', views.profile, name='profile'),
    path('all_topics/', views.all_topics, name='all_topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('like/<int:topic_id>/', views.like_topic, name='like_topic'),
    path('dislike/<int:topic_id>/', views.dislike_topic, name='dislike_topic'),
    path('comment/<int:topic_id>/', views.add_comment, name='add_comment'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('notifications/unread-count/', views.notification_unread_count, name='notification_unread_count'),
    path('notifications/list/', views.notification_list, name='notification_list'),
    path('notifications/mark-as-read/', views.notification_mark_as_read, name='notification_mark_as_read'),
    path('topic/<int:topic_id>/delete/', views.delete_topic, name='delete_topic'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('explore_topic/<int:topic_id>', views.explore_topic, name='explore_topic')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
