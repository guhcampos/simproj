from django.contrib import admin
from simproj.models import CashFlow, CashFlowSeries
from simproj.models import TesouroDireto

admin.site.register(CashFlowSeries)
admin.site.register(CashFlow)

admin.site.register(TesouroDireto)
