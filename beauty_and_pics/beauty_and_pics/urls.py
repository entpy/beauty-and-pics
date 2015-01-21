from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'beauty_and_pics.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^index/$', 'website.views.index', name='index'),
    url(r'^come-funziona/$', 'website.views.come_funziona', name='come_funziona'),
    url(r'^login/$', 'website.views.login', name='login'),
    url(r'^recupera-password/$', 'website.views.forgot_password', name='forgot_password'),
    url(r'^registrati/$', 'website.views.register', name='register'),
    url(r'^admin/', include(admin.site.urls)),
)
