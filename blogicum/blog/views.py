from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.consts import POSTS_ON_PAGE
from blog.forms import CommentForm, PostForm
from blog.models import Category, Comment, Post, User


class ListMixin:
    model = Post
    paginate_by = POSTS_ON_PAGE

    def get_queryset(self):
        return (
            Post.objects.select_related('author', 'location', 'category')
            .order_by('-pub_date')
            .annotate(comment_count=Count('comments'))
            .filter(
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True,
            )
        )


class PostListView(ListMixin, ListView):
    template_name = 'blog/index.html'


class CategoryPostListView(ListMixin, ListView):
    template_name = 'blog/category.html'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
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
        self.instance = get_object_or_404(
            User.objects.filter(username=self.kwargs.get('username'))
        )
        if self.instance != self.request.user:
            return super().get_queryset().filter(author=self.instance)
        else:
            return (
                Post.objects.select_related('author', 'location', 'category')
                .order_by('-pub_date')
                .annotate(comment_count=Count('comments'))
                .filter(author=self.instance)
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.instance
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    fields = (
        'first_name',
        'last_name',
        'username',
        'email',
    )
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        return self.request.user


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
                    & Q(pub_date__lte=timezone.now())
                    & Q(category__is_published=True)
                ),
                pk=self.kwargs.get('post_id'),
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.select_related('author').filter(
            post=self.kwargs.get('post_id')
        )
        return context


class PostCreateView(LoginRequiredMixin, PostFormMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostUpdateView(
    LoginRequiredMixin, PostFormMixin, PostEditMixin, UpdateView
):

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )


class PostDeleteView(LoginRequiredMixin, PostEditMixin, DeleteView):

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class CommentMixin:
    model = Comment
    form_class = CommentForm
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
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'post_id'
    commented_post = None

    def form_valid(self, form):
        self.commented_post = get_object_or_404(
            Post, pk=self.kwargs.get('post_id')
        )
        form.instance.author = self.request.user
        form.instance.post = self.commented_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):
    pass


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    pass
