from datetime import date, datetime, time
from functools import reduce
from typing import Any, Dict, List, Optional, Set, TypeVar
from urllib.parse import urlencode, urlparse

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import Model
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from rest_framework.reverse import reverse

from pytz import timezone


TZ = timezone(settings.TIME_ZONE)

COWSAY_TEMPLATE = r"""
##{speech_bubble_border}##
# {msg} #
##{speech_bubble_border}##
       \
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||"""


def add_safely_query_params(url: str, params: Dict[str, Any]) -> str:
    return url + ("&" if urlparse(url).query else "?") + urlencode(params)


def cowsay(msg: str, print_end: str = "\n\n") -> None:
    """
    Print ASCII picture of a cow saying something provided by the user.

    Refers to the true and original: https://en.wikipedia.org/wiki/Cowsay
    """
    speech_bubble_border = len(msg) * "#"
    formatted_cowsay_str = COWSAY_TEMPLATE.format(
        msg=msg, speech_bubble_border=speech_bubble_border
    )
    print(formatted_cowsay_str, end=print_end)


K = TypeVar("K")
V = TypeVar("V")


def extract_keys_from_dict(dict_: Dict[K, V], keys: Set[K]) -> Dict[K, V]:
    return {key: dict_[key] for key in keys}


def get_today_hh_mm(hh_mm: str) -> datetime:
    hh, mm = map(lambda x: int(x), hh_mm.split(":"))
    naive_datetime = datetime.combine(date=date.today(), time=time(hour=hh, minute=mm))
    return TZ.localize(naive_datetime)


def get_link_to_admin_form_for_object(obj: Model, inner_html: Optional[str] = None) -> str:
    path = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", args=[obj.id])
    if inner_html is None:
        inner_html = str(obj)
    link = format_html('<a href="{}">{}</a>', mark_safe(path), inner_html)  # nosec
    return link


def get_object_str(obj: object, attrs_to_show: List[Any]) -> str:
    class_name = obj.__class__.__name__

    attrs_reprs = []
    for attr in attrs_to_show:
        attr_value = reduce(lambda x, y: getattr(x, y), attr.split("."), obj)
        attr_repr = f"{attr}={attr_value!r}"
        attrs_reprs.append(attr_repr)

    return f'{class_name}({", ".join(attrs_reprs)})'


def humanize_seconds(seconds: float) -> str:
    """Seconds formatted for humans."""
    result = []
    seconds_rounded = int(round(seconds))

    if seconds_rounded == 0:
        return "less than or equal 0.5 seconds"

    for name, count in [["minutes", 60], ["seconds", 1]]:
        value = seconds_rounded // count
        if value:
            seconds_rounded -= value * count
            if value == 1:
                name = name.rstrip("s")
            result.append(f"{value} {name}")

    return ", ".join(result)


validate_url = URLValidator()


def is_valid_url(url: str) -> bool:
    try:
        validate_url(url)
    except ValidationError:
        return False
    return True
