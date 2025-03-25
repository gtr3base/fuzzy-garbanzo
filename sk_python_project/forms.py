from django import forms
from django.contrib.auth.models import User
from .models import Topic, Entry
from django.contrib.auth.forms import PasswordChangeForm

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text', 'is_private']
        labels = {'text':''}

    is_private = forms.BooleanField(required=False, initial=False, label="Make this topic private")


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}


class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'px-4 py-2 border rounded-lg'})


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'px-4 py-2 border rounded-lg'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'px-4 py-2 border rounded-lg'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'px-4 py-2 border rounded-lg'}))