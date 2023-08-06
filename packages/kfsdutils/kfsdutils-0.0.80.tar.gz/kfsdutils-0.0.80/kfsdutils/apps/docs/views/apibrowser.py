"""General API Views"""
from typing import Any

from django.urls import reverse
from kfsdutils.apps.frontend.views.basetemplateview import BaseTemplateView


class APIBrowserView(BaseTemplateView):
    """Show browser view based on rapi-doc"""

    template_name = "browser.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        path = self.request.build_absolute_uri(
            reverse("schema-api",)
        )
        return super().get_context_data(path=path, **kwargs)
