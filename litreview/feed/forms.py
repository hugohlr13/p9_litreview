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
        labels = {'title': 'Titre'}

RATING_CHOICES = [
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]

class ReviewForm(forms.ModelForm):

    rating = forms.TypedChoiceField(
        widget=forms.RadioSelect, choices=RATING_CHOICES, coerce=int
    )
    
    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
        labels = {'headline': 'Titre', 'rating': 'Note', 'body': 'Commentaire'}


