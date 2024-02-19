from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from blog.consts import POSTS_ON_PAGE
from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post


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
