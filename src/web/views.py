from django.shortcuts import render,get_object_or_404
from django.core.paginator import *
from posts.models import *
from django.contrib.postgres.search import *

def index(request):
    categories = Category.objects.all()[:5]
    authors = Author.objects.all()

    posts = Post.objects.filter(is_deleted=False, is_draft=False)
    q = request.GET.get('q')
    if q:
        vector = SearchVector("title",weight="A")+SearchVector("author__name",weight="B")+SearchVector("category__title",weight="C")
        query = SearchQuery(q)
        posts = posts.annotate( rank =SearchRank(vector,query)).filter(rank__gte=0.0001).order_by("-rank")
    # Filtering by author
    search_authors = request.GET.getlist("author")
    if search_authors:
        posts = posts.filter(author__id__in=search_authors)

    # Filtering by category
    search_categories = request.GET.getlist("category")
    if search_categories:
        posts = posts.filter(categories__id__in=search_categories).distinct()

    # Sorting by title
    sort = request.GET.get("sort")
    if sort:
        if sort == "title-asc":
            posts = posts.order_by("title")
        elif sort == "title-desc":
            posts = posts.order_by("-title")
        elif sort == "date-asc":
            posts = posts.order_by("published_date")
        elif sort == "date-desc":
            posts = posts.order_by("-published_date")
                
    # Pagination
    paginator = Paginator(posts, 4)  # Show 4 posts per page
    page_number = request.GET.get('page')
    try:
        instances = paginator.page(page_number)
    except PageNotAnInteger:
        instances = paginator.page(1)
    except EmptyPage:
        instances = paginator.page(paginator.num_pages)

    context = {
        "title": "Blog Post | Create your blog",
        "instances": instances,
        "categories": categories,
        "authors": authors,
        "posts": posts
    }
    return render(request, "web/index.html", context=context)

def post(request,id):
    instance= get_object_or_404(Post.objects.filter(id=id)) 
    categories = Category.objects.all()[:4]
    post_title = instance.title
    context={
        "instance":instance,
        'title':post_title,
        "categories": categories,
    }
    return render(request, "posts/post.html", context=context)
