from django.views.generic import TemplateView

from kfsdutils.apps.frontend.views.baseview import BaseView

class BaseTemplateView(BaseView, TemplateView):
    pass