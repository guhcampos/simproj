# -*- coding: utf-8 -*-
import datetime
import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from models import CashFlowSeries, CashFlow


def home(request):
    return render(request, "fluxo.html")


def post(request):

    data = json.loads(request.POST.get("req"))

    response = {}

    fs = CashFlowSeries()
    fs.project = data["conf"]["nome"]
    fs.use_selic = data["conf"]["selic"]
    fs.use_ipca = data["conf"]["ipca"]
    fs.use_igpm = data["conf"]["igpm"]
    fs.save()

    for flow in data["dados"]:

        f = CashFlow()
        f.series = fs
        f.description = flow[0]
        f.value = float(flow[2])
        f.date = datetime.datetime.strptime(flow[1], "%Y-%m-%d")
        f.discount(use_selic=fs.use_selic, use_ipca=fs.use_ipca, use_igpm=fs.use_igpm)
        f.save()

    fs.discounted = datetime.date.today()

    response["erro"] = False
    response["errormsg"] = None
    response["fluxos"] = fs.json()
    response["npv"] = float(fs.npv())
    response["irr"] = float(fs.irr())
    response["selic_periodo"] = "IMPLEMENTAR"
    response["npvplot"] = fs.npvplot()

    if settings.DEBUG:
        import pprint
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(response)

    return HttpResponse(json.dumps(response), content_type='application/json')
