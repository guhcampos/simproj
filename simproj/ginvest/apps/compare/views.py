# -*- coding: utf-8 -*-

import datetime
import json
import math
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from ginvest.apps.fluxo.models import CashFlowSeries
from ginvest.apps.tesouro.models import TesouroDireto
from ginvest.apps.poupanca.models import Poupanca
# Create your views here.


def home(request):

    response = {}

    response["titulos"] = [
        (titulo.id, "{} - Vencimento: {}".format(titulo.name, titulo.maturity))
        for titulo
        in TesouroDireto.objects.all()
    ]

    response["projetos"] = [
        (projeto.id, projeto.project)
        for projeto
        in CashFlowSeries.objects.all()
    ]

    return render(request, "compare.html", response)


def post(request):

    data = json.loads(request.POST.get("data"))
    response = {
        "chart_data": []
    }

    try:
        projeto = CashFlowSeries.objects.get(id=int(data["projeto_id"]))
        primeiro_fluxo = projeto.cashflows.all()[0]
        data_inicial = primeiro_fluxo.date
        data_final = projeto.cashflows.all().reverse()[0].date
        startvalue = math.fabs(primeiro_fluxo.npv)

        response["chart_data"].append(
            {
                "name": projeto.project,
                "values": projeto.compare_plot()
            }
        )

    except ObjectDoesNotExist:
        print("Nao deu certo")
        data_inicial = datetime.date.today()
        data_final = data_inicial + datetime.timedelta(days=360)
        startvalue = float(data["startvalue"].replace(",", "."))
        pass

    # Calculos Tesouro Direto
    for titulo in TesouroDireto.objects.all():

        titulo.profitability(
            startvalue,
            data_inicial,
            data_final
        )

        response["chart_data"].append(
            {
                "name": "{} [{}]".format(titulo.description, titulo.maturity),
                "values": titulo.profitability_chart(),
            }
        )

    # Calculos Poupanca
    poup = Poupanca()
    response["chart_data"].append(
        {
            "name": "Poupança",
            "values": list(poup.rendimentos(data_inicial, data_final, startvalue))
        }
    )
    if settings.DEBUG:
        import pprint
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(response)

    return HttpResponse(json.dumps(response), content_type='application/json')
