from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    Extends the default User model to store additional profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        """
        Returns the string representation of the profile.

        :return: Username of the linked user.
        """
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a UserProfile instance whenever a new User is created.

    :param sender: The model class sending the signal.
    :param instance: The actual instance being saved.
    :param created: Boolean flag indicating if a new record was created.
    :param kwargs: Additional keyword arguments.
    :return: None
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()