from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path(
        'profile/edit/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile',
    ),
    path(
        'profile/<slug:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
    path(
        '',
        views.IndexListView.as_view(),
        name='index'
    ),
    path(
        'posts/create/',
        views.PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/edit/',
        # views.post_edit,
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        'posts/<int:post_id>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:pk>/edit_comment/<comment_id>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<int:pk>/delete_comment/<comment_id>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
    path('category/<slug:category_slug>/',
         views.CategoryPostListView.as_view(),
         # views.category_posts,
         name='category_posts'
         ),
]