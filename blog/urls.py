from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterFormView.as_view(), name="register"),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/create/', views.CreatePost.as_view(), name='create-post'),
    path('mycomments/', views.MyCommentView.as_view(), name='my-comments'),
    path('comment/create/<int:pk>', views.CommentCreateView.as_view(), name='create-comment'),
    path('profiles/<int:pk>/', views.ProfileInfo.as_view(), name='user-detail'),
    path('profiles/', views.ProfileList.as_view(), name='profile-list'),
    path('contact/', views.MessageAdmin.as_view(), name='message-admin'),
    path('profiles/<int:pk>/update/', views.UserEditView.as_view(), name='user-update'),
    path('password_reset_confirm/<int:pk>', views.BloggerPasswordChangeView.as_view(), name='password_reset_confirm'),
    path('profiles/<int:pk>/', views.ProfileInfo.as_view(), name='profile-list'),
]
