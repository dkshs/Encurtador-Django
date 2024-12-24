# ruff: noqa: BLE001
from datetime import UTC
from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render

from sbily.utils.data import validate

from .models import ShortenedLink

LINK_BASE_URL = getattr(settings, "LINK_BASE_URL", None)


@login_required
def home(request):
    return render(request, "home.html", {"LINK_BASE_URL": LINK_BASE_URL})


@login_required
def create_link(request: HttpRequest):
    if request.method != "POST":
        return redirect("home")
    next_path = request.POST.get("next_path") or "home"
    original_link = request.POST.get("original_link") or ""
    shortened_link = request.POST.get("shortened_link") or ""
    is_temporary = request.POST.get("is_temporary") == "on"

    if not validate([original_link]):
        messages.error(request, "Please enter a valid original link")
        return redirect(next_path)

    try:
        link_data = {
            "original_link": original_link,
            "shortened_link": shortened_link,
            "user": request.user,
        }

        if is_temporary:
            link_data["remove_at"] = datetime.now(UTC) + timedelta(days=1)

        link = ShortenedLink.objects.create(**link_data)
        messages.success(request, "Link created successfully")
        return redirect("link", shortened_link=link.shortened_link)
    except ValidationError as e:
        messages.error(request, e.messages[0])
        return redirect(next_path)
    except Exception:
        messages.error(request, "An error occurred")
        return redirect(next_path)


def redirect_link(request, shortened_link):
    try:
        link = ShortenedLink.objects.get(shortened_link=shortened_link)
        if not link.is_functional():
            messages.error(request, "Link is expired or deactivated")
            if request.user == link.user:
                return redirect("link", link.shortened_link)
            return redirect("home")
        return redirect(link.original_link)
    except ShortenedLink.DoesNotExist:
        messages.error(request, "Link not found")
        return redirect("home")
    except Exception:
        messages.error(request, "An error occurred")
        return redirect("home")


@login_required
def link(request, shortened_link):
    try:
        link = ShortenedLink.objects.get(
            shortened_link=shortened_link,
            user=request.user,
        )

        deactivate = request.GET.get("deactivate")
        if deactivate is not None:
            deactivate = deactivate == "True" or False
            link.is_active = not deactivate
            link.save()
            messages.success(
                request,
                f"Link {'deactivated' if deactivate else 'activated'}",
            )
            return redirect("my_account")

        return render(
            request,
            "link.html",
            {"link": link, "LINK_BASE_URL": LINK_BASE_URL},
        )
    except ShortenedLink.DoesNotExist:
        messages.error(request, "Link not found")
        return redirect("home")
    except Exception:
        messages.error(request, "An error occurred")
        return redirect("home")


@login_required
def update_link(request, shortened_link):
    if request.method != "POST":
        return redirect("my_account")
    try:
        link = ShortenedLink.objects.get(
            shortened_link=shortened_link,
            user=request.user,
        )
        original_link = request.POST.get("original_link") or ""
        shortened_link = request.POST.get("shortened_link") or ""
        is_active = request.POST.get("is_active") == "on" or False
        is_temporary = request.POST.get("is_temporary") == "on" or False

        if not validate([original_link]):
            messages.error(request, "Please enter an original link")
            return redirect("link", link.shortened_link)

        if (
            original_link == link.original_link
            and shortened_link == link.shortened_link
            and is_active == link.is_active
            and is_temporary == (link.remove_at is not None)
        ):
            messages.warning(request, "No changes were made")
            return redirect("link", link.shortened_link)

        old_shortened_link = link.shortened_link
        link.original_link = original_link
        link.shortened_link = shortened_link
        link.is_active = is_active
        link.remove_at = datetime.now(UTC) + timedelta(days=1) if is_temporary else None
        link.save()

        messages.success(request, "Link updated successfully")
        return redirect("link", link.shortened_link)
    except ShortenedLink.DoesNotExist:
        messages.error(request, "Link not found")
        return redirect("my_account")
    except ValidationError as e:
        messages.error(request, e.messages[0])
        return redirect("link", old_shortened_link)
    except Exception:
        messages.error(request, "An error occurred")
        return redirect("home")


@login_required
def delete_link(request, shortened_link):
    try:
        link = ShortenedLink.objects.get(
            shortened_link=shortened_link,
            user=request.user,
        )
        link.delete()
        messages.success(request, "Link deleted successfully")
        return redirect("my_account")
    except ShortenedLink.DoesNotExist:
        messages.error(request, "Link not found")
        return redirect("my_account")
    except Exception:
        messages.error(request, "An error occurred")
        return redirect("home")
