from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class Post(models.Model):
    title = models.CharField(max_length=256, blank=False)
    text = RichTextField(blank=True, null=True)
    author = models.CharField(max_length=256, blank=True)
    published_date = models.DateTimeField(blank=True, null=True)
    pre_moderation = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def publish(self):
        self.publication_date = timezone.now()
        self.save()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    text = models.CharField(max_length=256)
    author = models.CharField(max_length=128)

