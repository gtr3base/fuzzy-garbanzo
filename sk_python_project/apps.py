import atexit

from django.apps import AppConfig

class SkPythonProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sk_python_project'

    def ready(self):
        self.add_example_topics()
        atexit.register(self.delete_example_topics)

    def add_example_topics(self):
        from .models import User, Topic
        user = User.objects.first()
        if user:
            topics = [
                "My Life`s journey",
                "Best Java Practices",
                "Java or Python?"
            ]
            for text in topics:
                Topic.objects.get_or_create(text=text, owner=user, is_private=False)

    def delete_example_topics(self):
        from .models import User, Topic

        Topic.objects.filter(text__startswith="Example Topic").delete()
