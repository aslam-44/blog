from django import forms
from posts.models import Post

class PostForm(forms.ModelForm):
    tags  = forms.CharField(widget = forms.TextInput(attrs={'class':"input"}))
   
    class Meta:
        model = Post
        exclude =  ("author","published_date","category","is_deleted")

        widgets = {
            "time_to_read": forms.TextInput(attrs={'class':"input"}),
            "title": forms.TextInput(attrs={'class':"input"}),
            "short_description": forms.Textarea(attrs={'class':"input"}),

        }
   
