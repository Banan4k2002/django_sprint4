from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from .models import Post, Category, User
import datetime


POSTS_ON_PAGE = 10


class PostMixin:
    model = Post
    queryset = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        pub_date__lte=datetime.datetime.now(),
        is_published=True,
        category__is_published=True,
    )


class PostListView(PostMixin, ListView):
    template_name = 'blog/index.html'
    paginate_by = POSTS_ON_PAGE


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'id'


class CategoryPostListView(ListView):
    template_name = 'blog/category.html'
    paginate_by = POSTS_ON_PAGE

    def get_queryset(self):
        return Post.objects.select_related(
            'author', 'location', 'category'
        ).filter(
            pub_date__lte=datetime.datetime.now(),
            is_published=True,
            category__slug=self.kwargs.get('category_slug')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category.objects.filter(
            is_published=True,
            slug=self.kwargs.get('category_slug'),
        ))
        return context


class UserPostListView(ListView):
    template_name = 'blog/profile.html'
    paginate_by = POSTS_ON_PAGE

    def get_queryset(self):
        return Post.objects.select_related(
            'author', 'location', 'category'
        ).filter(
            author__username=self.kwargs.get('username')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(User.objects.filter(
            username=self.kwargs.get('username')
        ))
        return context


class UserUpdateView(UpdateView):
    model = User
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    fields = ('first_name', 'last_name', 'username', 'email',)
    success_url = reverse_lazy('blog:index')
