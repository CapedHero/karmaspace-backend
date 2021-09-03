from django.db.models import QuerySet


def get_sort_index_for_first_position(queryset: QuerySet) -> float:
    lower_bound = 0.0
    upper_bound = (
        queryset.order_by("sort_index").values_list("sort_index", flat=True).first() or 1.0
    )
    return (lower_bound + upper_bound) / 2.0


def get_sort_index_for_last_position(queryset: QuerySet) -> float:
    lower_bound = queryset.order_by("sort_index").values_list("sort_index", flat=True).last() or 0.0
    upper_bound = 1.0
    return (lower_bound + upper_bound) / 2.0
