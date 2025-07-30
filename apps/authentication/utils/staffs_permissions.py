from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


def setup_staff_group_permissions():
    # Trying to get the 'staff' group, if it doesn't exist, create it
    staff_group, created = Group.objects.get_or_create(name="staff")

    # If the group is newly created or has no permissions, assign the necessary permissions
    if created or staff_group.permissions.count() == 0:
        model_perms = {
            "plan": ["add", "change", "delete", "view"],
            "subscription": ["view"],
            "exchangeratelog": ["view"],
        }

        for model_name, actions in model_perms.items():
            try:
                model = apps.get_model(app_label="services", model_name=model_name)
                content_type = ContentType.objects.get_for_model(model)

                for action in actions:
                    codename = f"{action}_{model_name}"
                    permission = Permission.objects.filter(
                        codename=codename, content_type=content_type
                    ).first()
                    if permission:
                        staff_group.permissions.add(permission)

            except LookupError:
                pass

    return staff_group
