from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from .forms import TicketForm, ReviewForm, FollowUsersForm
from .models import Ticket, Review, UserFollows
from .utils import get_users_viewable_tickets, get_users_viewable_reviews


@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user) 
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True
    )

    return render(request, 'feed/feed.html', {'posts': posts})

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
    review_form = ReviewForm()
    ticket_form = TicketForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        if all((review_form.is_valid(), ticket_form.is_valid())):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    else:
        review_form = ReviewForm()
        ticket_form = TicketForm()
    return render(request, 'feed/create_review.html', {'review_form': review_form, 'ticket_form': ticket_form})

@login_required
def review_snippet(request, review_id):
    review = Review.objects.get(id=review_id)
    return render(request, 'feed/review_snippet.html', {'review': review})

@login_required
def ticket_snippet(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'feed/ticket_snippet.html', {'ticket': ticket})


@login_required
def follow_users(request):
    form = FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            followed_user = form.cleaned_data['followed_user']
            user_follows, created = UserFollows.objects.get_or_create(
                user=request.user,
                followed_user=followed_user
            )
            if created:
                # Si l'objet a été créé, vous pouvez effectuer d'autres actions si nécessaire
                pass
            return redirect('home')
    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    return render(request, 'feed/follow_users.html', context={'form': form, 'following': following, 'followers': followers})





