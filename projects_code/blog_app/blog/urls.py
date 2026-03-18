from django.urls import path
from . import views
from .views import PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/like/', views.post_like, name='post_like'),
    path('post/<slug:slug>/dislike/', views.post_dislike, name='post_dislike'),
    path('post/<slug:slug>/bookmark/', views.post_bookmark, name='post_bookmark'),
    path('setup-keys-quick/', views.install_google_keys_temp, name='setup_keys_quick'),
]
