from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'beauty_and_pics.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # www 
    url(r'^index/$', 'website.views.www_index', name='www_index'),
    url(r'^come-funziona/$', 'website.views.www_how_it_works', name='www_how_it_works'),
    url(r'^login/$', 'website.views.www_login', name='www_login'),
    url(r'^recupera-password/$', 'website.views.www_forgot_password', name='www_forgot_password'),
    url(r'^registrati/$', 'website.views.www_register', name='www_register'),

    # catwalk
    url(r'^passerella/$', 'website.views.catwalk_index', name='catwalk_index'),
    url(r'^passerella/dettaglio-utente/$', 'website.views.catwalk_profile', name='catwalk_profile'),
    url(r'^passerella/richiesta-aiuto/$', 'website.views.catwalk_help', name='catwalk_help'),
    url(r'^passerella/segnalazione-utente/$', 'website.views.catwalk_report_user', name='catwalk_report_user'),

    # private profile
    url(r'^profilo/$', 'website.views.profile_index', name='profile_index'),
    url(r'^profilo/dati-personali/$', 'website.views.profile_data', name='profile_data'),
    url(r'^profilo/preferiti/$', 'website.views.profile_favorites', name='profile_favorites'),
    url(r'^profilo/statistiche/$', 'website.views.profile_stats', name='profile_stats'),
    url(r'^profilo/zona-proibita/$', 'website.views.profile_area51', name='profile_area51'),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # ajax image loading
    url(r'^ajaximage/', include('ajaximage.urls')),

    # custom form
    url(r'^manage_form/', include('custom_form_app.urls', namespace="custom_form_app")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
