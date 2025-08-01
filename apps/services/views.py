from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render

User = get_user_model()


def subscriptions(request):
    username_filter = request.GET.get("username", "").strip()

    users_qs = User.objects.all()
    if username_filter:
        users_qs = users_qs.filter(username__icontains=username_filter)
    users_qs = users_qs.prefetch_related("subscriptions__plan")

    paginator = Paginator(users_qs, 5)
    page_number = request.GET.get("page")
    users_page = paginator.get_page(page_number)

    return render(
        request,
        "services/subscriptions.html",
        {
            "users": users_page,
        },
    )
