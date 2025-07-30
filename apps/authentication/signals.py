from django.contrib.auth.models import Group, User
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.authentication.utils.staffs_permissions import setup_staff_group_permissions


@receiver(post_save, sender=User)
def manage_staff_group(sender, instance, created, **kwargs):
    """Add or remove staff group based on is_staff flag, ignoring superusers."""

    # Ignore superusers (do not change groups here)
    if instance.is_superuser:
        return

    # Get or create the staff group with permissions
    staff_group = Group.objects.filter(name="staff").first()
    if not staff_group:
        staff_group = setup_staff_group_permissions()

    def update_groups():
        if instance.is_staff:
            # Add to staff group if not already in
            if staff_group not in instance.groups.all():
                instance.groups.add(staff_group)
        else:
            # Remove from staff group if present and no longer staff
            if staff_group in instance.groups.all():
                instance.groups.remove(staff_group)

    # Use transaction.on_commit to ensure the group is added after the transaction is committed
    transaction.on_commit(update_groups)
