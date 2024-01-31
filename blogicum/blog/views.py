from django.shortcuts import get_object_or_404, render
from .models import Post, Category
import datetime


POSTS_ON_HOMEPAGE = 5


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        pub_date__lte=datetime.datetime.now(),
        is_published=True,
        category__is_published=True,
    )[
        :POSTS_ON_HOMEPAGE
    ]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('author', 'location', 'category'),
        pk=id,
        pub_date__lte=datetime.datetime.now(),
        is_published=True,
        category__is_published=True,
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        pub_date__lte=datetime.datetime.now(),
        is_published=True,
        category__slug=category_slug,
    )
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)
