from django import forms
from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ["first_name","last_name","email","username","password"]
            widgets = {
                  "password": forms.widgets.PasswordInput(attrs={"placeholder":"Enter your password" }),
                  "email": forms.widgets.EmailInput(attrs={"placeholder":"Enter your Email" })
                  

            }
