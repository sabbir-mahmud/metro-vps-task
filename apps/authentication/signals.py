from django.contrib.auth.models import Group, User
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.authentication.utils.staffs_permissions import setup_staff_group_permissions


@receiver(post_save, sender=User)
def enable_permissions_for_staffs(sender, instance, created, *args, **kwargs):
    """Enabling permissions for staff users."""

    # If the user is not a staff or superuser, do nothing
    # This is to ensure that only staff users get the permissions
    if not instance.is_staff or instance.is_superuser:
        return

    # Get or create the staff group
    # If the group does not exist, it will be created with the necessary permissions
    staff_group = Group.objects.filter(name="staff").first()
    if not staff_group:
        staff_group = setup_staff_group_permissions()

    def add_group_after_commit():
        if staff_group not in instance.groups.all():
            instance.groups.add(staff_group)

    # Use transaction.on_commit to ensure the group is added after the transaction is committed
    transaction.on_commit(add_group_after_commit)
