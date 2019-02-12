import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render("tesouro.html")


def post(request):

    data = json.loads(request.POST.get("data"))

    print(data)

    response = {}

    return HttpResponse(response, mimetype='application/json')
