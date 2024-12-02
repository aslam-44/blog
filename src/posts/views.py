
import datetime
import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator

from posts.forms import PostForm
from posts.models import Post, Author, Category
from main.decorators import allow_self

# Rest of your code remains the same
@login_required(login_url="/users/login/")
def create_post(request):
    if request.method == 'POST':
        print(request.POST)  # Print the request data
        print(request.FILES)  # Print the request files
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            tags = form.cleaned_data['tags']

            if not Author.objects.filter(user=request.user).exists():
                author = Author.objects.create(user=request.user, name=request.user.username)
            else:
                author = request.user.author

            instance = form.save(commit=False)
            instance.published_date = datetime.date.today()
            instance.author = author
            instance.save()

            tags_list = tags.split(",")

            for tag in tags_list:
                category, created = Category.objects.get_or_create(title=tag.strip())
                instance.category.add(category)

            response_data = {
                "title": "Post Created successfully",
                "message": "Post is uploaded",
                "status": "success",
                "redirect": "yes",
                "redirect_url": "/",
            }

        else:
            # Form is invalid, return an error response
            response_data = {
                "title": "Post Creation Failed",
                "message": "Please correct the errors in the form.",
                "status": "error",

            }
            print(form.errors)  # Print the form errors
        return HttpResponse(json.dumps(response_data))
    else:
        data = {
            "title": "Blog Title",
            "description": "Blog description",
            "short_description": "short description",
            "time_to_read": "8 min",
            "tags": "Technology,Computer,Coding",
        }
        form = PostForm(initial=data)
        context = {
            "title": "Create new post",
            "form": form
        }
        return render(request, "posts/create.html", context=context)



def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    
   
    context = {
        'post':post,
        
    }
    return render(request, 'posts/post.html', context=context)
@login_required(login_url="/users/login/")
def my_posts(request):
    instances = Post.objects.filter(author__user = request.user , is_deleted = False)
    context = {
        "title":"My Posts",
        "instances" : instances,
    }
    return render(request, 'posts/my-posts.html', context=context)

@login_required(login_url="/users/login/")
@allow_self

def delete_post(request, id):
    instance = get_object_or_404(Post, id=id, author__user=request.user)  # Ensure the post exists and belongs to the user
    instance.is_deleted = True
    instance.save()

    response_data = {
        "title": "Successfully Deleted",
        "message": "Post is deleted",
        "status": "success",
    }
    return JsonResponse(response_data)

@login_required(login_url="/users/login/")
@allow_self
def draft_post(request, id):
    instance = get_object_or_404(Post, id=id, author__user=request.user)  
    instance.is_draft = not instance.is_draft
    instance.save()

    response_data = {
        "title": "Successfully Changed",
        "message": "Post is updated successfully",
        "status": "success",
    }
    return JsonResponse(response_data) 
@login_required(login_url="/users/login/")
@allow_self
def edit_post(request, id):
    instance = get_object_or_404(Post, id=id, author__user=request.user)
    
    if request.method == 'POST':
        print(request.POST)  # Print the request data
        print(request.FILES)  # Print the request files
        form = PostForm(request.POST, request.FILES, instance=instance)  # Pass the instance here
        
        if form.is_valid():
            tags = form.cleaned_data['tags']
            
            if not Author.objects.filter(user=request.user).exists():
                author = Author.objects.create(user=request.user, name=request.user.username)
            else:
                author = request.user.author

            instance = form.save(commit=False)
            instance.save()

            tags_list = tags.split(",")
            
            # Clear existing categories and add new ones
            instance.category.clear()
            for tag in tags_list:
                category, created = Category.objects.get_or_create(title=tag.strip())
                instance.category.add(category)

            response_data = {
                "title": "Post Created successfully",
                "message": "Post is uploaded",
                "status": "success",
                "redirect": "yes",
                "redirect_url": "/",
            }
        else:
            # Form is invalid, return an error response
            response_data = {
                "title": "Post Creation Failed",
                "message": "Please correct the errors in the form.",
                "status": "error",
            }
            print(form.errors)  # Print the form errors
        return HttpResponse(json.dumps(response_data))

    else:
        # Get categories from the post instance
        categories = instance.category.all()
        category_string = ",".join([category.title for category in categories])

        form = PostForm(instance=instance, initial={"tags": category_string})
        context = {
            "title": "Edit post",
            "form": form,
        }
        return render(request, "posts/create.html", context=context)


