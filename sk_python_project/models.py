from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='topic_images/',
        blank=True,
        null=True,
        help_text='Upload an image for this topic'
    )
    video = models.FileField(
        upload_to='topic_videos/',
        blank=True,
        null=True,
        help_text='Upload a video for this topic',
        validators=[
            FileExtensionValidator(allowed_extensions=['mp4','mov','avi','webm'])
        ]
    )

    class Meta:
        permissions = [
            ("can_delete_any_topic", "Can delete any topic"),
            ("can_view_all_topics", "Can view all topics (including private)"),
            ("can_edit_any_topic", "Can edit any topic"),
        ]

    def __str__(self):
        return self.text


class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
        permissions = [
            ("can_delete_any_entry", "Can delete any entry"),
            ("can_edit_any_entry", "Can edit any entry"),
        ]

    def __str__(self):
        return f"{self.text[:50]}..."


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user} likes {self.topic}"


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user} dislikes {self.topic}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.topic}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, default='acted')
    text = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.text:
            if self.action == 'comment':
                self.text = f"{self.sender.username} commented on your topic '{self.topic.text}'"
            elif self.action == 'like':
                self.text = f"{self.sender.username} liked your topic '{self.topic.text}'"
            elif self.action == 'dislike':
                self.text = f"{self.sender.username} disliked your topic '{self.topic.text}'"
            else:
                self.text = f"{self.sender.username} {self.action} your topic '{self.topic.text}'"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender} {self.action} on {self.topic}"