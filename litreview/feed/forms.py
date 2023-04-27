from django import forms
from .models import Ticket, Review, UserFollows
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowUsersForm(forms.ModelForm):
    followed_user = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = User
        fields = ['followed_user']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

class ReviewForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    description = forms.CharField(max_length=2048, widget=forms.Textarea)
    image = forms.ImageField(required=False)
    rating = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = forms.CharField(max_length=128)
    body = forms.CharField(max_length=8192, widget=forms.Textarea)

    class Meta:
        model = Review
        fields = ('title', 'description', 'image', 'rating', 'headline', 'body')



