from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Profile


# @receiver(post_save, sender=User)
# def create_profile_on_user_creation(sender, instance, *args, **kwargs):
#     # creates a profile if one does not exist
#     profile,  created = Profile.objects.get_or_create(user=instance)
#     profile.save()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
