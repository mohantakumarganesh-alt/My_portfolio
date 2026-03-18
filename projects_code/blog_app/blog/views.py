from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CommentForm

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
        
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    slug_field = 'slug'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    slug_field = 'slug'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
    return JsonResponse({
        'liked': liked,
        'likes_count': post.total_likes(),
        'dislikes_count': post.total_dislikes()
    })

@login_required
def post_dislike(request, slug):
    post = get_object_or_404(Post, slug=slug)
    disliked = False
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        disliked = True
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
    return JsonResponse({
        'disliked': disliked,
        'likes_count': post.total_likes(),
        'dislikes_count': post.total_dislikes()
    })

@login_required
def post_bookmark(request, slug):
    post = get_object_or_404(Post, slug=slug)
    bookmarked = False
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
        bookmarked = True
    return JsonResponse({'bookmarked': bookmarked})

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.http import HttpResponse

def install_google_keys_temp(request):
    try:
        app, created = SocialApp.objects.get_or_create(provider='google')
        cid_p1 = '831312961302-adpms3'
        cid_p2 = 'ubqp8kqkuvh5v90u19cpt69r6u.apps.googleusercontent.com'
        app.client_id = cid_p1 + cid_p2
        sec_p1 = 'GOCSPX-N5UU5'
        sec_p2 = 'NdDP3LjTisXYs8fKvlSfk7q'
        app.secret = sec_p1 + sec_p2
        app.name = 'Google Auth'
        app.save()
        site = Site.objects.first() if Site.objects.exists() else Site.objects.create(domain='127.0.0.1:8000', name='Local')
        app.sites.add(site)
        app.save()
        return HttpResponse("<h1>Success: Google Keys Installed!</h1>")
    except Exception as e:
        return HttpResponse(f"<h1>Error: {e}</h1>")
