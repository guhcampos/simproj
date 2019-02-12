from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='tesouro-home'),
    url(r'post/$', views.post, name='tesouro-post')
)
