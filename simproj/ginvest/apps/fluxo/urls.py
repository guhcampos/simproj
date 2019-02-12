from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='fluxo-home'),
    url(r'post/$', views.post, name='fluxo-post')
)
