from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from illallangi.data.aviation.models import Airline


@require_GET
def airline_html(
    request: HttpRequest,
    airline_slug: str,
    **_: dict,
) -> render:
    objects = Airline.objects.filter(iata=airline_slug.upper())

    if objects.count() > 1:
        return HttpResponse(
            status=500,
            content="Multiple airlines found for slug",
        )

    if objects.count() == 1:
        obj = objects.first()
        return render(
            request,
            "aviation/airline.html",
            {
                "base_template": ("partial.html" if request.htmx else "base.html"),
                "obj": obj,
                "breadcrumbs": [
                    {
                        "title": "Airlines",
                        "url": reverse(
                            "airlines_html",
                        ),
                    },
                    {
                        "title": str(obj),
                        "url": obj.get_absolute_url(),
                    },
                ],
                "links": [
                    {
                        "rel": "alternate",
                        "type": "text/html",
                        "href": request.build_absolute_uri(
                            obj.get_absolute_url(),
                        ),
                    },
                ],
            },
        )

    return HttpResponse(
        status=400,
        content="Airline not found",
    )
