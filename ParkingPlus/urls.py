from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ParkingPlus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ParkingApp.views.home', name='home'),
    url(r'^carentry/', 'ParkingApp.views.carentry', name='carentry'),
    url(r'^exit/', 'ParkingApp.views.carsearch', name='exit'),
    url(r'^carexit/', 'ParkingApp.views.carexit', name='carexit'),
    url(r'^report/', 'ParkingApp.views.report', name='report'),
    url(r'^getreport/', 'ParkingApp.views.getreport', name='getreport'),
)
