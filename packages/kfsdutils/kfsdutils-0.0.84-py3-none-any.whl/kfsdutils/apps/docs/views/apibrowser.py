"""General API Views"""
from typing import Any

from django.urls import reverse
from kfsdutils.apps.frontend.views.basetemplateview import BaseTemplateView
from kfsdutils.apps.frontend.permissions.common import SignInRequired

class APIBrowserView(BaseTemplateView):
    """Show browser view based on rapi-doc"""

    template_name = "browser.html"
    permission_classes = [SignInRequired]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        path = self.request.build_absolute_uri(
            reverse("schema-api",)
        )
        return super().get_context_data(path=path, **kwargs)
