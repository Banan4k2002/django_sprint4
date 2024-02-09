import datetime

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Category, User, Comment
from .forms import PostForm, CommentForm
from .consts import POSTS_ON_PAGE


class ListMixin:
    model = Post
    paginate_by = POSTS_ON_PAGE
    queryset = (
        Post.objects.select_related('author', 'location', 'category')
        .order_by('-pub_date')
        .annotate(comment_count=Count('comments'))
    )


class PostListView(ListMixin, ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                is_published=True,
                pub_date__lte=datetime.datetime.now(),
                category__is_published=True,
            )
        )


class CategoryPostListView(ListMixin, ListView):
    template_name = 'blog/category.html'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                pub_date__lte=datetime.datetime.now(),
                is_published=True,
                category__slug=self.kwargs.get('category_slug'),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.filter(
                is_published=True,
                slug=self.kwargs.get('category_slug'),
            )
        )
        return context


class UserPostListView(ListMixin, ListView):
    template_name = 'blog/profile.html'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(author__username=self.kwargs.get('username'))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User.objects.filter(username=self.kwargs.get('username'))
        )
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    fields = (
        'first_name',
        'last_name',
        'username',
        'email',
    )
    success_url = reverse_lazy('blog:index')


class PostFormMixin:
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditMixin:
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        if instance.author != request.user:
            return redirect('blog:post_detail', self.kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            get_object_or_404(
                Post.objects.filter(
                    Q(author=request.user)
                    | Q(is_published=True)
                    & Q(pub_date__lte=datetime.datetime.now())
                    & Q(category__is_published=True)
                ),
                pk=self.kwargs.get('post_id'),
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.select_related(
            'post', 'author'
        ).filter(post=self.kwargs.get('post_id'))
        return context


class PostCreateView(LoginRequiredMixin, PostFormMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user}
        )


class PostUpdateView(
    LoginRequiredMixin, PostFormMixin, PostEditMixin, UpdateView
):

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )


class PostDeleteView(LoginRequiredMixin, PostEditMixin, DeleteView):

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user}
        )


class CommentMixin:
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Comment.objects.filter(post=self.kwargs.get('post_id')),
            pk=self.kwargs.get('comment_id'),
        )
        if instance.author != request.user:
            return redirect('blog:post_detail', self.kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )


class CommentFormMixin:
    commented_post = None
    form_class = CommentForm

    def form_valid(self, form):
        self.commented_post = get_object_or_404(
            Post, pk=self.kwargs.get('post_id')
        )
        form.instance.author = self.request.user
        form.instance.post = self.commented_post
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CommentFormMixin, CreateView):
    model = Comment
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )


class CommentUpdateView(
    LoginRequiredMixin, CommentMixin, CommentFormMixin, UpdateView
):
    pass


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    pass
