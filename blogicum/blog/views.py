import datetime as dt

from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import PostForm, CommentForm, UserForm
from .models import Post, Category, Comment, User


# Константа для пагинации:
PAGINATOR_POSTS = 10


def const_post():
    """ Функция-константа для публикаций.

    Запрашивает все публикации, согласно фильтрации, сортирует
    по дате от новых к старым и получает число комментариев к
    каждой публикации.
    """
    return (
        Post.objects.select_related(
            'author',
            'location',
            'category'
        ).order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comments')
        )
    )


class CommentPermissionMixin:
    """ Класс-миксин, для проверки авторства комментария.

    При несовпадении автора перенаправляет на страницу публикации,
    которой принадлежит комментарий.
    """
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Comment,
            pk=kwargs['comment_id']
        )
        if instance.author != request.user:
            return redirect(
                'blog:post_detail',
                self.kwargs['pk']
            )
        return super().dispatch(request, *args, **kwargs)


class PostPermissionMixin:
    """ Класс-миксин, для проверки авторства публикации.

    При несовпадении автора перенаправляет на страницу редактируемой
    публикации.
    """
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Post,
            pk=kwargs['post_id']
        )
        if instance.author != self.request.user:
            return redirect(
                'blog:post_detail',
                self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


# ================ работа с публикациями ========================

class IndexListView(ListView):
    """ Вывод публикаций на главную страницу.

    Класс выводящий все публикации, отсортированные по дате от новых
    к старым, с пагинацией 10 публикаций на странице.
    """
    model = Post
    template_name = 'blog/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(
            const_post().filter(
                category__is_published=True,
                is_published=True,
                pub_date__lte=dt.datetime.now(),
            ), PAGINATOR_POSTS
        )
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class PostDetailView(DetailView):
    """ Представление отдельной публикации.

    Класс выводящий отдельную публикацию с формой для ввода комментария
    любым авторизованным пользователем. Проверка на авторство для
    возможности редактирования/удаления отложенных, снятых с публикации
    постов.
    """
    pk_url_kwarg = 'post_id'
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['object'].author != self.request.user:
            filter_user = {
                'pub_date__lte': dt.datetime.now(),
                'is_published': True,
                'category__is_published': True,
            }
        else:
            filter_user = {}
        get_object_or_404(
            Post,
            pk=self.kwargs['post_id'],
            **filter_user,
        )
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related(
            'author'
        ).order_by(
            'created_at'
        )
        return context


class PostUpdateView(
    PostPermissionMixin,
    LoginRequiredMixin,
    UpdateView
):
    """ Редактирование отдельной публикации.

    Класс выводящий форму для редактирования публикации. Проверка
    на авторство через PostPermissionMixin.
    """
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(
    PostPermissionMixin,
    LoginRequiredMixin,
    DeleteView
):
    """ Удаление публикации.

    Класс выводящий форму для удаления публикации. Проверка на
    авторство через PostPermissionMixin.
    """
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:index')


class PostCreateView(
    LoginRequiredMixin,
    CreateView
):
    """ Создание публикации.

    Класс выводящий форму для создания публикации, любым
    авторизованным пользователем.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class CategoryPostListView(ListView):
    """ Вывод публикаций в выбранной категории.

    Класс выводящий публикации в выбранной пользователем категории,
    отсортированные по дате от новых к старым. С пагинацией 10
    публикаций на станицу.
    """
    model = Category
    slug_field = 'category_slug'
    slug_url_kwarg = 'category_slug'
    template_name = 'blog/category.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug']
        )
        paginator = Paginator(
            const_post().filter(
                category__id=category.id,
                is_published=True,
                pub_date__lte=dt.datetime.now()
            ), PAGINATOR_POSTS
        )
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['category'] = category
        context['page_obj'] = page_obj
        return context


# ============ Работа с профилем пользователя ===================

class ProfileDetailView(ListView):
    """ Вывод страницы с информацией о пользователе.

    Класс выводящий информацию о запрошенном пользователе и список
    его опубликованных записей с сортировкой по дате от новых к старым,
    с пагинаций 10 публикаций на страницу, доступно любому посетителю
    блога. Для автора отображаются снятые с публикации и отложенные записи.
    """
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'blog/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        if context['profile'] != self.request.user:
            filter_user = {
                'is_published': True,
                'pub_date__lte': dt.datetime.now(),
            }
        else:
            filter_user = {}
        paginator = Paginator(
            const_post().filter(
                author=context['profile'],
                **filter_user,
            ).order_by('-pub_date'), PAGINATOR_POSTS
        )
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(
    LoginRequiredMixin,
    UpdateView
):
    """ Редактирование данных пользователя.

    Класс выводящий форму для редактирования данных авторизованного
    пользователя.
    """
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


# ============ Работа с комментариями ==========================

class CommentCreateView(
    LoginRequiredMixin,
    CreateView
):
    """ Создание комментария.

    Класс выводящий форму для создания комментария, любым авторизованным
    пользователем.
    """
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentUpdateView(
    CommentPermissionMixin,
    LoginRequiredMixin,
    UpdateView
):
    """ Редактирование комментария.

    Класс выводящий форму для редактирования комментария. Проверка на
    авторство через CommentPermissionMixin.
    """
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['pk']}
        )


class CommentDeleteView(
    CommentPermissionMixin,
    LoginRequiredMixin,
    DeleteView
):
    """ Удаление комментария.

    Класс выводящий форму для удаления комментария. Проверка на
    авторство через CommentPermissionMixin.
    """
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['pk']}
        )
