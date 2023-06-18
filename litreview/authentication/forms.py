from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    """Form to log in a user : username and password"""

    username = forms.CharField(max_length=63, label="Nom d’utilisateur")
    password = forms.CharField(
        max_length=63, widget=forms.PasswordInput, label="Mot de passe"
    )


class SignupForm(UserCreationForm):
    """Form to sign up a user : username, password and password confirmation"""
    
    username = forms.CharField(
        label="",
        max_length=150,
        help_text="",
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}),
    )
    password1 = forms.CharField(
        label="",
        help_text="",
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
    )
    password2 = forms.CharField(
        label="",
        help_text="",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmation du mot de passe"}
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", "password1", "password2"]
