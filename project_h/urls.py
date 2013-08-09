from django.conf.urls import patterns, include, url
from userena import urls
from reservar import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_h.views.home', name='home'),
    # url(r'^project_h/', include('project_h.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(urls)),
    url(r'^token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^reservar/api/reservar$',views.reservar_sala.as_view()),
    url(r'^reservar/api/listreserv$', views.listreservas.as_view()),
    url(r'^reservar/sala$',views.reserv_sala),
    url(r'^reservar/sala/update$',views.reservar_salaupdate.as_view()),
    url(r'^reservar/sala/delete$',views.reservar_saladelete.as_view()),
    url(r'^reservar/show/(\d+)$',views.show_reserv_sala)
)
