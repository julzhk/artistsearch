from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'search.views.home_page', name='home'),
    url(r'^api', 'search.views.api_page', name='api'),
    url(r'^admin/', include(admin.site.urls)),
]
