from django.conf import settings
from PIL import Image
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings


class Ticket(models.Model):
    """Model to represent a ticket."""

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Review(models.Model):
    """Model to represent a review."""

    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE, blank=True, null=True
    )
    rating = models.PositiveSmallIntegerField(
        max_length=1024,
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    """Model to represent a user following another user."""

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers_by",
    )

    class Meta:
        unique_together = (
            "user",
            "followed_user",
        )
