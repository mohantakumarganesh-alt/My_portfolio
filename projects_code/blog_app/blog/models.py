from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    content = CKEditor5Field('Content', config_name='extends')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='post_bookmarks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def read_time(self):
        # Average reading speed: 200 words per minute
        word_count = len(self.content.split())
        minutes = word_count / 200
        return max(1, round(minutes))

    def total_likes(self):
        return self.likes.count()
        
    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

@receiver(pre_save, sender=Post)
def create_post_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
        # Handle duplicates
        original_slug = instance.slug
        queryset = Post.objects.filter(slug=original_slug).exclude(pk=instance.pk)
        count = 1
        while queryset.exists():
            instance.slug = f"{original_slug}-{count}"
            queryset = Post.objects.filter(slug=instance.slug).exclude(pk=instance.pk)
            count += 1
