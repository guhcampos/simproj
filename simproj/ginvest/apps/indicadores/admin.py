from django.contrib import admin

from models import SELIC
from models import IGPM
from models import IPCA

admin.site.register(SELIC)
admin.site.register(IGPM)
admin.site.register(IPCA)
