import pytest
from django.core.paginator import Paginator
from django.http import QueryDict
from django.shortcuts import render

from cast.models import Blog


def test_pagination_template_is_not_paginated(simple_request):
    r = render(simple_request, "cast/plain/pagination.html", {})
    html = r.content.decode("utf-8").strip()
    assert html == ""


def test_pagination_template_is_paginated(simple_request):
    r = render(simple_request, "cast/plain/pagination.html", {"is_paginated": True})
    html = r.content.decode("utf-8").strip()
    assert "pagination" in html


def test_pagination_template_is_paginated_long(simple_request):
    paginator = Paginator(range(1000), 2)
    page = paginator.page(9)
    context = {
        "is_paginated": page.has_other_pages(),
        "paginator": paginator,
        "page_obj": page,
        "object_list": page.object_list,
        "page_range": page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1),
    }
    r = render(simple_request, "cast/plain/pagination.html", context)
    html = r.content.decode("utf-8").strip()
    assert "page=1" in html  # first page
    assert "page=500" in html  # last page

    # two ellipsis in the middle which are not links
    ellipsis_items = [line for line in html.splitlines() if "…" in line]
    assert len(ellipsis_items) == 2
    assert (
        '<span class="page-link">…</span>' == ellipsis_items[0].strip()
    )  # ellipsis in the middle which is not a link


@pytest.mark.parametrize(
    "query_string, expected_other_get_params",
    [
        ("", ""),
        ("foo=bar&bar=foo&page=3", "&foo=bar&bar=foo"),
    ],
)
def test_get_other_get_params(query_string, expected_other_get_params):
    assert Blog.get_other_get_params(QueryDict(query_string)) == expected_other_get_params
