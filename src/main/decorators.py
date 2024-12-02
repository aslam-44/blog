import json
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from posts.models import Post

def allow_self(function):
    def wrapper(request, *args, **kwargs):
        id = kwargs["id"]
        # Check if the post exists and the author is the logged-in user
        if not Post.objects.filter(id=id, author__user=request.user).exists():
            # Handle Ajax request (usually for front-end API requests)
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                response_data = {
                    "status": "error",
                    "title": "Unauthorized Access",
                    "message": "Unauthorized Access"
                }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                return HttpResponseRedirect(reverse("web:index"))
        
        return function(request, *args, **kwargs)
    
    return wrapper
