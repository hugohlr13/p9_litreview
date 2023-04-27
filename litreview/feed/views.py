from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm, FollowUsersForm
from .models import Ticket, Review, UserFollows

@login_required
def home(request):
    tickets = Ticket.objects.all()
    return render(request, 'feed/home.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    else:
        form = TicketForm()
    return render(request, 'feed/create_ticket.html', {'form': form})

@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = Ticket.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data.get('image'),
                user=request.user
            )
            review = Review.objects.create(
                ticket=ticket,
                rating=form.cleaned_data['rating'],
                headline=form.cleaned_data['headline'],
                body=form.cleaned_data['body'],
                user=request.user
            )
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'feed/create_review.html', {'form': form})

@login_required
def follow_users(request):
    form = FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            user_follows = UserFollows.objects.create(
                user=request.user,
                followed_user=form.cleaned_data['followed_user']
            )
            user_follows.save()
            return redirect('home')
    return render(request, 'feed/follow_users.html', context={'form': form})


@login_required
def following_list(request):
    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    return render(request, 'feed/following_list.html', {'following': following, 'followers': followers})


