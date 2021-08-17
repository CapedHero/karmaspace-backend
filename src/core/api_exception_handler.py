from typing import Any, Dict, Optional

from django.core.exceptions import ValidationError as DJValidationError
from django.http import Http404, HttpResponse
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.fields import get_error_detail
from rest_framework.views import exception_handler


def api_exception_handler(exc: Exception, context: Dict[str, Any]) -> Optional[HttpResponse]:
    if isinstance(exc, DJValidationError):
        errors = get_error_detail(exc)
        exc = DRFValidationError(errors)
    if isinstance(exc, Http404) and str(exc):
        exc = NotFound(str(exc))
    response = exception_handler(exc, context)
    return response
