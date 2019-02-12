from django.conf.urls import patterns, include, url
from django.contrib import admin

from simproj import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^simulation/post/', views.SimulationPostView.as_view(), name='newsim-post'),    
    url(r'^simulation/', views.SimulationView.as_view(), name='newsim-home'),
    url(r'^fixedincome/post/', views.FixedIncomePostView.as_view(), name='fixedincome-post'),
    url(r'^fixedincome/', views.FixedIncomeView.as_view(), name='fixedincome-home'),
    url(r'^financing/post/', views.FinancingPostView.as_view(), name='financing-post'),
    url(r'^financing/', views.FinancingView.as_view(), name='financing-home'),

    # Third Party Apps 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)
