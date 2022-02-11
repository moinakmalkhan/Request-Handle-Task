from enum import Enum

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import HttpResponse

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class NumOfReqEnum(Enum):
    GOLD = 10
    SILVER = 5
    BRONZE = 2


class RequestHandelMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        if cache.get(get_client_ip(request)) is None:
            num_of_req = 1
            if request.user.is_authenticated:
                groups = request.user.groups.all()
                if groups.exists():
                    for group in groups:
                        req = NumOfReqEnum[group.name.upper()].value
                        if num_of_req < req:
                            num_of_req = req

            cache.set(get_client_ip(request), num_of_req, CACHE_TTL)
        else:
            data = int(cache.get(get_client_ip(request)))
            if data <= 0:
                return HttpResponse("You are blocked to send request")
            cache.set(get_client_ip(request), data - 1, CACHE_TTL)

        response = self.get_response(request)
        return response
