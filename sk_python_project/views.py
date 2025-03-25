from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Topic, Entry, Comment, Like, Dislike
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import UsernameChangeForm, CustomPasswordChangeForm


def index(request):
    return render(request, 'sk_python_project/index.html')


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
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'sk_python_project/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('sk_python_project:topics')


    context = {'form':form}
    return render(request,'sk_python_project/new_topic.html', context)


def all_topics(request):
    topics = Topic.objects.filter(is_private=False)

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
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('sk_python_project:topic', topic_id=topic_id)


    context = {'topic': topic, 'form': form}
    return render(request, 'sk_python_project/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404


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
    return redirect('sk_python_project:all_topics')

@login_required
def dislike_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if not Dislike.objects.filter(user=request.user, topic=topic).exists():
        Dislike.objects.create(user=request.user, topic=topic)
        Like.objects.filter(user=request.user, topic=topic).delete()
    return redirect('sk_python_project:all_topics')

@login_required
def add_comment(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(user=request.user, topic=topic, text=comment_text)
    return redirect('sk_python_project:all_topics')