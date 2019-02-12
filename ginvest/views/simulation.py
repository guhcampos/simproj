# -*- coding: utf-8 -*-
import datetime
import json
from django.conf import settings
from django.views.generic import TemplateView
from simproj.models import CashFlowSeries, CashFlow
from simproj.views import JSONResponseView


class SimulationView(TemplateView):
    template_name = "simulation.html"

class SimulationPostView(JSONResponseView):
    
    def get_context_data(self, *args, **kwargs):

        self.context = dict()
        
        request_data = json.loads(self.request.POST.get("req"))

        fs = CashFlowSeries()
        fs.use_selic = request_data["conf"]["selic"]
        fs.use_ipca = request_data["conf"]["ipca"]
        fs.use_igpm = request_data["conf"]["igpm"]
        fs.save()

        for flow in request_data["dados"]:

            f = CashFlow()
            f.series = fs
            f.description = flow[0]
            f.value = float(flow[2])
            f.date = datetime.datetime.strptime(flow[1], "%Y-%m-%d")
            f.discount(use_selic=fs.use_selic, use_ipca=fs.use_ipca, use_igpm=fs.use_igpm)
            f.save()

        fs.discounted = datetime.date.today()

        self.context["erro"] = False
        self.context["errormsg"] = None
        self.context["fluxos"] = fs.json()
        self.context["npv"] = float(fs.npv())
        self.context["irr"] = float(fs.irr())
        self.context["selic_periodo"] = "IMPLEMENTAR"
        self.context["npvplot"] = fs.npvplot()

        return self.context