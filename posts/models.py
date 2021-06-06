# models.py
from django.db import models
from django.conf import settings

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.timezone import now


# Post, Comment 각각의 Model에는 id가 부여되고, 이것을 urls.py에서는 post_id, comment_id로 사용한다.

class Post(models.Model):
    subject = models.CharField(max_length=50, blank=True)
    content = models.CharField(max_length=300, blank=True)
    image = models.ImageField(blank=True, upload_to='posts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    created = models.DateTimeField(default=now, editable=False)
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
    created = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.id}: {self.content} - {self.user.username}"
