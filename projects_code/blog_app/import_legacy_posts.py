import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from blog.models import Post

User = get_user_model()
try:
    author = User.objects.get(username='admin')
except User.DoesNotExist:
    author = User.objects.first()

posts_data = [
    {
        "title": "Getting Started with Django",
        "content": "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development...",
        "image_url": "https://images.unsplash.com/photo-1504639725590-34d0984388bd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Why Python for Backend?",
        "content": "Python is one of the most popular programming languages today, especially for backend development. Its readability, vast ecosystem of libraries, and frameworks like Django and Flask make it a top choice...",
        "image_url": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
    }
]

for data in posts_data:
    post, created = Post.objects.update_or_create(
        title=data['title'],
        defaults={
            'content': data['content'],
            'author': author,
            'image_url': data['image_url']
        }
    )
    if created:
        print(f"Created post: {post.title}")
    else:
        print(f"Updated post: {post.title}")
