from django.contrib.auth.models import User

def is_admin(user):
    return user.is_staff or user.has_perm('sk_python_project.can_delete_any_topic')

def can_view_all_topics(user):
    return user.is_staff or user.has_perm('sk_python_project.can_view_all_topics')

def can_edit_any_topic(user):
    return user.is_staff or user.has_perm('sk_python_project.can_edit_any_topic')

def can_edit_any_entry(user):
    return user.is_staff or user.has_perm('sk_python_project.can_edit_any_entry')