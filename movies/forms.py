from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, MovieRating


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "gender", "phone", "birth_date")
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = MovieRating
        fields = ("rating",)
