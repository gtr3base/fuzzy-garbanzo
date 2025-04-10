from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .admin_utils import can_view_all_topics, is_admin
from .models import Topic, Entry, Comment, Like, Dislike, Notification
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import UsernameChangeForm, CustomPasswordChangeForm


def index(request):
    unread_count = 0
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'sk_python_project/index.html', {'unread_count': unread_count})


@login_required
def topics(request):
    query = request.GET.get('q', '')
    if query:
        topics = Topic.objects.filter(text__icontains=query, owner=request.user, is_private=True)
    else:
        topics = Topic.objects.filter(owner=request.user, is_private=False)

    return render(request, 'sk_python_project/topics.html', {'topics': topics, 'query': query})


@login_required
def profile(request):
    if request.method == 'POST' and 'change_username' in request.POST:
        username_form = UsernameChangeForm(request.POST, instance=request.user)
        if username_form.is_valid():
            username_form.save()
            return redirect('sk_python_project:profile')
    else:
        username_form = UsernameChangeForm(instance=request.user)

    if request.method == 'POST' and 'change_password' in request.POST:
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return redirect('sk_python_project:profile')
    else:
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'sk_python_project/profile.html', {
        'username_form': username_form,
        'password_form': password_form,
    })


@login_required
def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.is_private and topic.owner != request.user:
        raise PermissionDenied("You dont have permission to view this topic")
    #if not (topic.owner == request.user or can_view_all_topics(request.user)):
    #    raise Http404

    entries = topic.entry_set.order_by('-date_added')
    comments = topic.comment_set.order_by('-created_at')

    context = {
        'topic': topic,
        'entries': entries,
        'comments': comments,
    }
    return render(request, 'sk_python_project/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('sk_python_project:topics')


    context = {'form':form}
    return render(request,'sk_python_project/new_topic.html', context)


def all_topics(request):
    topics = Topic.objects.filter(is_private=False).order_by('-date_added')

    query = request.GET.get('q')
    if query:
        topics = topics.filter(text__icontains=query)

    return render(request, 'sk_python_project/all_topics.html', {'topics': topics})


@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        if topic.owner != request.user:
            raise PermissionDenied('You dont have permission to perform this action')

        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('sk_python_project:topic', topic_id=topic_id)


    context = {'topic': topic, 'form': form}
    return render(request, 'sk_python_project/new_entry.html', context)


def explore_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    entries = topic.entry_set.order_by('-date_added')
    comments = topic.comment_set.order_by('-created_at')

    context = {
        'topic': topic,
        'entries': entries,
        'comments': comments,
    }
    return render(request, 'sk_python_project/explore_topic.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise PermissionDenied('You dont have permission to perform this action')

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('sk_python_project:topic', topic_id=topic.id)

    context={'entry':entry,'topic':topic,'form':form}
    return render(request, 'sk_python_project/edit_entry.html', context)


@login_required
def like_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if not Like.objects.filter(user=request.user, topic=topic).exists():
        Like.objects.create(user=request.user, topic=topic)
        Dislike.objects.filter(user=request.user, topic=topic).delete()

        if topic.owner != request.user:
            Notification.objects.create(
                recipient=topic.owner,
                sender=request.user,
                topic=topic,
                action='like'
            )
            send_notification(topic.owner.id)

    next_url = request.POST.get('next', request.GET.get('next', 'sk_python_project:all_topics'))
    return redirect(next_url)


@login_required
def dislike_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if not Dislike.objects.filter(user=request.user, topic=topic).exists():
        Dislike.objects.create(user=request.user, topic=topic)
        Like.objects.filter(user=request.user, topic=topic).delete()

        if topic.owner != request.user:
            Notification.objects.create(
                recipient=topic.owner,
                sender=request.user,
                topic=topic,
                action='dislike'
            )
            send_notification(topic.owner.id)

    next_url = request.POST.get('next', request.GET.get('next', 'sk_python_project:all_topics'))
    return redirect(next_url)


@login_required
def add_comment(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(user=request.user, topic=topic, text=comment_text)

            if topic.owner != request.user:
                notification_text = f"{request.user.username} commented on your topic '{topic.text}': {comment_text[:50]}{'...' if len(comment_text) > 50 else ''}"
                Notification.objects.create(
                    recipient=topic.owner,
                    sender=request.user,
                    topic=topic,
                    action='comment',
                    text=notification_text
                )
                send_notification(topic.owner.id, text=notification_text, topic=topic.text)

    next_url = request.POST.get('next', request.GET.get('next', 'sk_python_project:all_topics'))
    return redirect(next_url)


def send_notification(user_id, text=None, topic=None):
    channel_layer = get_channel_layer()
    count = Notification.objects.filter(recipient_id=user_id, is_read=False).count()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user_id}",
        {
            'type': 'send.notification',
            'unread_count': count,
            'message': 'You have a new notification!',
            'text': text,
            'topic': topic
        }
    )


@login_required
def notification_unread_count(request):
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'count': count})


@login_required
def notification_list(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)

    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:10]

    return render(request, 'sk_python_project/notification_list.html', {
        'notifications': notifications
    })


@login_required
def notification_mark_as_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})


@staff_member_required
def admin_dashboard(request):
    recent_topics = Topic.objects.order_by('-date_added')[:10]
    recent_entries = Entry.objects.order_by('-date_added')[:10]
    unread_notifications = Notification.objects.filter(is_read=False).count()
    user_count = User.objects.count()
    private_topics_count = Topic.objects.filter(is_private=True).count()
    total_likes = Like.objects.count()
    total_comments = Comment.objects.count()

    context = {
        'recent_topics': recent_topics,
        'recent_entries': recent_entries,
        'unread_notifications': unread_notifications,
        'user_count': user_count,
        'private_topics_count': private_topics_count,
        'total_likes': total_likes,
        'total_comments': total_comments,
    }
    return render(request, 'sk_python_project/dashboard.html', context)


@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if not (is_admin(request.user) or topic.owner == request.user):
        raise Http404

    if request.method == 'POST':
        topic_name = topic.text
        topic.delete()
        messages.success(request, f"Topic '{topic_name}' was deleted successfully.")
        next_url = request.POST.get('next', request.GET.get('next', 'sk_python_project:admin_dashboard'))
        return redirect(next_url)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'confirm_delete.html', {'object': topic})

    return render(request, 'sk_python_project/confirm_delete.html', {'topic': topic})


@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if not (is_admin(request.user) or topic.owner == request.user):
        raise Http404

    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Entry was deleted successfully.")
        next_url = request.POST.get('next', request.GET.get('next', 'sk_python_project:admin_dashboard'))
        return redirect(next_url)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'admin/confirm_delete_entry.html', {'object': entry})

    return render(request, 'sk_python_project/confirm_delete_entry.html', {'entry': entry})