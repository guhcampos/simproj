from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='indicadores-home'),
    url(r'post/$', views.post, name='indicadores-post')
)
