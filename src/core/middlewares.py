import sys
from typing import Callable

from django.http import HttpRequest, HttpResponse

from better_exceptions import excepthook


class BetterExceptionsMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def process_exception(self, request: HttpRequest, exception: Exception) -> None:
        excepthook(exception.__class__, exception, sys.exc_info()[2])
        return None
