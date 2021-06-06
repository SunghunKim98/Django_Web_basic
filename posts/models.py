# models.py
from django.db import models
from django.conf import settings

from django.db.models.signals import post_delete
from django.dispatch import receiver


class Post(models.Model):
    content = models.CharField(max_length=300, blank=True)
    image = models.ImageField(blank=True, upload_to='posts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_posts", blank=True)

    def __str__(self):
        return f"{self.id}: {self.content}"

@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

class Comment(models.Model):
    content = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.id}: {self.content} - {self.user.username}"
