from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Extends the built-in User model with additional profile attributes.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        """
        Returns the string representation of the profile.

        :return: Username of the associated user.
        """
        return self.user.username


class Category(models.Model):
    """
    Represents an ad category with a unique name constraint.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def get_active_ads_count(self):
        """
        Calculates the total number of active ads in the category.

        :return: Total count of active advertisements.
        """
        return self.ads.filter(is_active=True).count()

    def __str__(self):
        """
        Returns the string representation of the category.

        :return: Name of the category.
        """
        return self.name


class Ad(models.Model):
    """
    Represents an advertisement item posted by a user.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads')

    def short_description(self):
        """
        Provides a truncated version of the description.

        :return: The first 100 characters of the description.
        """
        return self.description[:100]

    def deactivate_if_expired(self):
        """
        Deactivates the advertisement if it has expired.

        :return: None
        """
        if self.created_at and timezone.now() > self.created_at + timedelta(days=30):
            self.is_active = False
            self.save()

    def __str__(self):
        """
        Returns the string representation of the advertisement.

        :return: Title of the advertisement.
        """
        return self.title


class Comment(models.Model):
    """
    Represents a feedback comment linked to a specific advertisement.
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    @classmethod
    def get_comments_count_for_ad(cls, ad_id):
        """
        Counts comments assigned to a specific advertisement.

        :param ad_id: The ID of the targeted advertisement.
        :return: Total number of comments.
        """
        return cls.objects.filter(ad_id=ad_id).count()

    def __str__(self):
        """
        Returns the string representation of the comment.

        :return: Contextual label indicating user and ad title.
        """
        return f"Comment by {self.user.username} on {self.ad.title}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signals the creation of a profile immediately after a user is saved.

    :param sender: The model class sending the signal.
    :param instance: The actual instance of the user being saved.
    :param created: Boolean flag indicating if a new record was created.
    :param kwargs: Additional keyword arguments.
    :return: None
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Ad)
def check_ad_expiration_signal(sender, instance, **kwargs):
    """
    Signals validation before saving an ad to auto-deactivate if it is older than 30 days.

    :param sender: The model class sending the signal.
    :param instance: The actual instance of the advertisement being saved.
    :param kwargs: Additional keyword arguments.
    :return: None
    """
    if instance.id and instance.created_at:
        if timezone.now() > instance.created_at + timedelta(days=30):
            instance.is_active = False
