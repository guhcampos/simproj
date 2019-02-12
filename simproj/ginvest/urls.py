from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('ginvest.apps.core.urls')),
    url(r'^fluxo/', include('ginvest.apps.fluxo.urls')),
    url(r'^compare/', include('ginvest.apps.compare.urls')),
    url(r'^indicadores/', include('ginvest.apps.indicadores.urls')),
    url(r'^tesouro/', include('ginvest.apps.tesouro.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)
