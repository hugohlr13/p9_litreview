from .models import Review, Ticket, UserFollows


def get_users_viewable_tickets(user):
    """Return a queryset of tickets that the user can see"""

    # Retourne un queryset de tickets que l'utilisateur peut voir
    # Utilise les informations stockées dans UserFollows pour récupérer les tickets
    # l'utilisateur peut également voir ses propres tickets
    followed_users = UserFollows.objects.filter(user=user).values_list(
        "followed_user", flat=True
    )
    tickets = Ticket.objects.filter(user__in=followed_users) | Ticket.objects.filter(
        user=user
    )
    tickets = tickets.exclude(review__isnull=False) 
    return tickets.distinct()


def get_users_viewable_reviews(user):
    """Return a queryset of reviews that the user can see"""
    
    followed_users = UserFollows.objects.filter(user=user).values_list(
        "followed_user", flat=True
    )
    reviews = Review.objects.filter(user__in=followed_users) | Review.objects.filter(
        user=user
    )
    return reviews.distinct()

