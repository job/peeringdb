import os

from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from django.urls import reverse, resolve

from rest_framework.viewsets import ModelViewSet

from peeringdb_server import settings


def on(timeout=None):
    """
    turns maintenance mode on

    Keyword Arguments:

        - timeout<int=None>: if specified will automatically
            end maintenance mode after n seconds
    """
    open(settings.MAINTENANCE_MODE_LOCKFILE, "ab", 0).close()


def off():
    """ turn maintenance mode off """
    if active():
        os.remove(settings.MAINTENANCE_MODE_LOCKFILE)


def active():
    """ return True if maintenance mode is currently active """
    return os.path.isfile(settings.MAINTENANCE_MODE_LOCKFILE)


def raise_if_active():
    """ raise ActionBlocked exception if maintenance mode is active """
    if active():
        raise ActionBlocked()


class Middleware(object):

    """
    Middleware will return 503 json responses for all write
    ops (POST PUT PATCH DELETE)
    """

    def process_request(self, request):
        if not active():
            return None

        if request.method.lower() in ["post", "put", "patch", "delete"]:

            view, args, kwargs = resolve(request.path_info)

            if view.func_name in ["request_login"]:
                # login should be allowed even in maint. mode
                return None
            elif hasattr(view, "cls") and issubclass(view.cls, ModelViewSet):
                # api response
                return JsonResponse(
                    {"meta": {"error": str(ActionBlocked())}}, status=503
                )
            else:
                # other
                fn, args, kwargs = resolve(reverse("maintenance"))
                return JsonResponse(
                    {"non_field_errors": [str(ActionBlocked())]}, status=503
                )
        else:
            return None


class ActionBlocked(Exception):
    def __init__(self):
        super(ActionBlocked, self).__init__(
            "The site is currently in maintenance mode, during which this action is disabled, please try again in a few minutes"
        )
