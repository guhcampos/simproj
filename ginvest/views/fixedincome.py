import datetime
import json
from django.conf import settings
from django.views.generic import TemplateView
from simproj.views import JSONResponseView
from simproj.models import TesouroDireto

class FixedIncomeView(TemplateView):

    template_name = "fixedincome.html"

    def get_context_data(self, *args, **kwargs):

        self.context = super(FixedIncomeView, self).get_context_data(*args, **kwargs)
        
        self.context["titulos"] = [
            (titulo.id, "{} - Vencimento: {}".format(titulo.name, titulo.maturity))
            for titulo
            in TesouroDireto.objects.all()
        ]

        return self.context

class FixedIncomePostView(JSONResponseView):
    
    def get_context_data(self, *args, **kwargs):

        self.context = dict()

        request_data = json.loads(self.request.POST.get("data"))

        startvalue = float(request_data["startvalue"].replace(",", "."))
        #custody = float(request_data["custody"].replace(",", "."))

        paper = TesouroDireto.objects.get(id=int(request_data["titulo"]))
        paper.profitability(startvalue, datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=360*2))

        self.context["chart_data"] = (
                {
                    "name": "Teste",
                    "values": paper.profitability_chart()
                },
            )

        return self.context