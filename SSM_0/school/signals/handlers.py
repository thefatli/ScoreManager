from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from school.models import Student, Teacher

# 检查是哪种
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        if instance.identified_check == 'A':
            instance.is_staff = True
            instance.save()