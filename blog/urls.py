from django.urls import path
from blog import views


app_name = 'blog'
urlpatterns = [
	path('', views.RedirectUserView.as_view(), name='redirect'),
    path('post', views.PostListView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user-posts'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.About.as_view(), name='blog-about')
]
