from django.views.generic import ListView, DetailView
from .models import Post, Category
import datetime


POSTS_ON_HOMEPAGE = 5

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
    paginate_by = POSTS_ON_HOMEPAGE


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'id'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    queryset = Category.objects.filter(
        is_published=True,
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.select_related(
            'author', 'location', 'category'
        ).filter(
            pub_date__lte=datetime.datetime.now(),
            is_published=True,
            category__slug=self.kwargs.get('category_slug'),
        )
        return context
