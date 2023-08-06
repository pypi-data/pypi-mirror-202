from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponseForbidden
from django.utils.crypto import constant_time_compare


class SentrySecureSourceMapMiddleware:
    def __init__(self, get_response):
        if not settings.SENTRY_SECURITY_TOKEN:
            raise MiddlewareNotUsed

        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(settings.STATIC_URL) and request.path.endswith(
            ".map"
        ):
            sentry_token = request.headers.get("X-Sentry-Token", "")

            if not constant_time_compare(sentry_token, settings.SENTRY_SECURITY_TOKEN):
                return HttpResponseForbidden()

        return self.get_response(request)
