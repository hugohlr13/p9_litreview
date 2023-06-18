from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm, TicketForm, UserSearchForm
from .models import Review, Ticket, UserFollows
from .utils import get_users_viewable_reviews, get_users_viewable_tickets


@login_required
def feed(request):
    """Display the user's feed."""

    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    return render(request, "feed/feed.html", {"posts": posts})


@login_required
def create_ticket(request):
    """Create a ticket."""

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home")
    else:
        form = TicketForm()
    return render(request, "feed/create_ticket.html", {"form": form})


@login_required
def create_review(request):
    """Create a review."""

    review_form = ReviewForm()
    ticket_form = TicketForm()
    if request.method == "POST":
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
            return redirect("home")
    else:
        review_form = ReviewForm()
        ticket_form = TicketForm()
    return render(
        request,
        "feed/create_review.html",
        {"review_form": review_form, "ticket_form": ticket_form},
    )


@login_required
def review_snippet(request, review_id):
    """Display a review."""

    review = Review.objects.get(id=review_id)
    return render(request, "feed/review_snippet.html", {"review": review})


@login_required
def ticket_snippet(request, ticket_id):
    """Display a ticket."""

    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, "feed/ticket_snippet.html", {"ticket": ticket})


@login_required
def create_review_to_ticket(request, ticket_id):
    """Create a review to a ticket."""

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if Review.objects.filter(ticket=ticket).exists():
        # Vous pouvez choisir de rediriger l'utilisateur vers une autre page
        # ou afficher un message d'erreur ici
        return redirect("home")  # rediriger vers la page d'accueil par exemple
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")
    else:
        form = ReviewForm()
    return render(request, "feed/create_review_to_ticket.html", {"form": form})


@login_required
def my_posts(request):
    """Display the user's posts."""

    reviews = Review.objects.filter(user=request.user).annotate(
        content_type=Value("REVIEW", CharField())
    )
    tickets = Ticket.objects.filter(user=request.user).annotate(
        content_type=Value("TICKET", CharField())
    )
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )
    return render(request, "feed/post.html", {"posts": posts})


@login_required
def edit_review(request, review_id):
    """Edit a review."""

    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("my_posts")
    else:
        form = ReviewForm(instance=review)
    return render(request, "feed/edit_review.html", {"form": form})


@login_required
def delete_review(request, review_id):
    """Delete a review."""

    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == "POST":
        review.delete()
        return redirect("my_posts")
    return render(request, "feed/delete_review.html", {"review": review})


@login_required
def edit_ticket(request, ticket_id):
    """Edit a ticket."""

    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("my_posts")
    else:
        form = TicketForm(instance=ticket)
    return render(request, "feed/edit_ticket.html", {"form": form})


@login_required
def delete_ticket(request, ticket_id):
    """Delete a ticket."""

    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == "POST":
        ticket.delete()
        return redirect("my_posts")
    return render(request, "feed/delete_ticket.html", {"ticket": ticket})


User = get_user_model()


@login_required
def follow_users(request):
    """Follow users."""
    
    search_form = UserSearchForm()
    searched_users = User.objects.none()
    search_performed = False
    if request.method == "POST":
        if "username" in request.POST:  # searching for users
            search_form = UserSearchForm(request.POST)
            if search_form.is_valid():
                searched_users = User.objects.filter(
                    username__icontains=search_form.cleaned_data["username"]
                )
                search_performed = True
        elif "follow" in request.POST:  # following a user
            followed_user = User.objects.get(id=request.POST["follow"])
            user_follows, created = UserFollows.objects.get_or_create(
                user=request.user, followed_user=followed_user
            )
        elif "unfollow" in request.POST:  # unfollowing a user
            unfollowed_user = User.objects.get(id=request.POST["unfollow"])
            user_follows = UserFollows.objects.filter(
                user=request.user, followed_user=unfollowed_user
            )
            user_follows.delete()
    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    return render(
        request,
        "feed/follow_users.html",
        context={
            "search_form": search_form,
            "searched_users": searched_users,
            "following": following,
            "followers": followers,
            "search_performed": search_performed,
        },
    )
