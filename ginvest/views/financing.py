from django.views.generic import TemplateView
from simproj.views import JSONResponseView


class FinancingView(TemplateView):

    template_name = "financing.html"

class FinancingPostView(JSONResponseView):
    pass