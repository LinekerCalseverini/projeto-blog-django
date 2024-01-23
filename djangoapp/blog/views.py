from typing import Any
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView

PER_PAGE = 9


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()  # type: ignore

    # def get_queryset(self):
    #     queryset = super().get_queryset().filter(is_published=True)
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })
        return context


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = f'Posts de {user_full_name} - '

        ctx.update({
            'page_title': page_title
        })

        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user
        })

        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        category_name = self.object_list[0].category.name  # type:ignore
        page_title = f'{category_name} - Categoria - '

        ctx.update({
            'page_title': page_title
        })

        return ctx


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        category_name = self.object_list[0].tags.filter(  # type:ignore
            slug=self.kwargs.get('slug')
        ).first().name
        page_title = f'{category_name} - Tag - '

        ctx.update({
            'page_title': page_title
        })

        return ctx


def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = (
        Post.objects.get_published()  # type: ignore
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    page_title = f'{search_value} - Search - '

    if len(search_value) > 30:
        page_title = f'{search_value[:30]}... - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'search_value': search_value,
            'page_title': page_title,
        }
    )


def page(request, slug):
    page_obj = (
        Page.objects  # type: ignore
        .filter(is_published=True)
        .filter(slug=slug).first()
    )

    if page_obj is None:
        raise Http404()

    page_title = f'{page_obj.title} - Página - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )


def post(request, slug):
    post_obj = (
        Post.objects.get_published()  # type: ignore
        .filter(slug=slug).first()
    )

    if post_obj is None:
        raise Http404()

    page_title = f'{post_obj.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
