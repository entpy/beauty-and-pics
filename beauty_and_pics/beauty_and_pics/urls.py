from django.conf.urls import include, url
from django.contrib import admin
from adminplus.sites import AdminSitePlus
from django.conf import settings
from django.conf.urls.static import static

# admin to add custom view
admin.site = AdminSitePlus()
admin.autodiscover()

# errors
handler404 = 'website.views.custom404_view'
handler500 = 'website.views.custom500_view'

urlpatterns = [
    # www 
    url(r'^$', 'website.views.www_index', name='www_index'),
    url(r'^index/$', 'website.views.www_index', name='www_index'),
    url(r'^login/$', 'website.views.www_login', name='www_login'),
    url(r'^logout/$', 'website.views.www_logout', name='www_logout'),
    url(r'^recupera-password/$', 'website.views.www_forgot_password', name='www_forgot_password'),
    url(r'^registrati/$', 'website.views.www_register', name='www_register'),
    url(r'^registrazione-rapida/(?:(?P<user_id>\d+)/)?$', 'website.views.www_fast_register', name='www_fast_register'),
    url(r'^privacy/$', 'website.views.www_privacy', name='www_privacy'),
    url(r'^termini-di-utilizzo/$', 'website.views.www_terms', name='www_terms'),
    url(r'^cookie-policy/$', 'website.views.www_cookie_policy', name='www_cookie_policy'),
    url(r'^come-funziona/$', 'website.views.www_how_it_works_info', name='www_how_it_works_info'),
    url(r'^come-iscriversi/$', 'website.views.www_signup_info', name='www_signup_info'),
    url(r'^il-concorso/$', 'website.views.www_contest_info', name='www_contest_info'),
    url(r'^classifica/(?P<contest_type>[a-z-]+)/(?:(?P<contest_year>\d+)/)?$', 'website.views.www_ranking_contest', name='www_ranking_contest'), # pagina con la classifica del concorso
    url(r'^podio/(?P<contest_type>[a-z-]+)/(?P<contest_year>\d+)/(?P<user_id>\d+)/?$', 'website.views.www_podium', name='www_podium'), # pagina podio per i primi 5 utenti
    url(r'^caratteristiche/$', 'website.views.www_features', name='www_features'),
    url(r'^faq/$', 'website.views.www_faq', name='www_faq'),
    # activate account
    url(r'^conferma-email/(?P<auth_token>\w+)/$', 'website.views.www_email_confirm', name='www_email_confirm'),
    url(r'^email-confermata/$', 'website.views.www_email_successfully_confirmed', name='www_email_successfully_confirmed'),
    # howto
    url(r'^howto/le-votazioni/$', 'website.views.www_howto_votations', name='www_howto_votations'),
    url(r'^howto/concorsi-a-tema/$', 'website.views.www_howto_photocontest', name='www_howto_photocontest'),

    # catwalk
    url(r'^concorsi-a-tema/$', 'website.views.catwalk_photo_contest_list', name='catwalk_photo_contest_list'), # elenco di tutti i photocontest
    url(r'^concorsi-a-tema/(?P<photocontest_code>[a-z-]+)/$', 'website.views.catwalk_photo_contest_pics', name='catwalk_photo_contest_pics'), # elenco di immagini per un determinato photocontest
    url(r'^concorsi-a-tema/(?P<photocontest_code>[a-z-]+)/(?P<user_id>\d+)/$', 'website.views.catwalk_photo_contest_pics_info', name='catwalk_photo_contest_pics_info'), # dettaglio immagine di un certo photocontest
    url(r'^passerella/dettaglio-utente/(?P<user_id>\d+)/$', 'website.views.catwalk_profile', name='catwalk_profile'),
    url(r'^passerella/richiesta-aiuto/$', 'website.views.catwalk_help', name='catwalk_help'),
    url(r'^passerella/segnalazione-utente/(?P<user_id>\d+)/$', 'website.views.catwalk_report_user', name='catwalk_report_user'),
    url(r'^passerella/donna/$', 'website.views.catwalk_index', {"contest_type": "woman-contest"}, name='catwalk_index'),
    url(r'^passerella/uomo/$', 'website.views.catwalk_index', {"contest_type": "man-contest"}, name='catwalk_index'),
    url(r'^passerella/(?:(?P<contest_type>[a-z-]+)/)?$', 'website.views.catwalk_index', name='catwalk_index'), # per il blocco catwalk questo va messo sempre al fondo

    # private profile
    url(r'^profilo/(?:(?P<welcome>\d+)/)?$', 'website.views.profile_index', name='profile_index'),
    url(r'^profilo/dati-personali/$', 'website.views.profile_data', name='profile_data'),
    url(r'^profilo/preferiti/$', 'website.views.profile_favorites', name='profile_favorites'),
    url(r'^profilo/statistiche/$', 'website.views.profile_stats', name='profile_stats'),
    url(r'^profilo/zona-proibita/$', 'website.views.profile_area51', name='profile_area51'),
    url(r'^profilo/pannello-di-controllo/$', 'website.views.profile_control_panel', name='profile_control_panel'),
    url(r'^profilo/avvisi/$', 'website.views.profile_advise', name='profile_advise'),
    url(r'^profilo/notifiche/(?:(?P<notify_id>\d+)/)$', 'website.views.profile_notify_details', name='profile_notify_details'),
    url(r'^profilo/notifiche/$', 'website.views.profile_notify', name='profile_notify'),
    url(r'^profilo/ottieni-punti/$', 'website.views.profile_gain_points', name='profile_gain_points'),
    url(r'^profilo/ottieni-premio/$', 'website.views.profile_get_prize', name='profile_get_prize'),
    url(r'^profilo/intervista/$', 'website.views.profile_interview', name='profile_interview'),
    url(r'^profilo/pubblicazione-intervista/$', 'website.views.profile_interview_publishing', name='profile_interview_publishing'),
    # django_photo_contest
    url(r'^profilo/concorsi-a-tema/$', 'website.views.profile_photo_contest_list', name='profile_photo_contest_list'),
    url(r'^profilo/concorsi-a-tema/(?P<photocontest_code>[a-z-]+)/seleziona-foto/$', 'website.views.profile_photo_contest_select', name='profile_photo_contest_select'),
    url(r'^profilo/concorsi-a-tema/(?P<photocontest_code>[a-z-]+)/$', 'website.views.profile_photo_contest_info', name='profile_photo_contest_info'),

    # email test
    url(r'^email-test/(?P<email_name>\w+)/(?P<email_mode>\w+)/$', 'website.views.email_test', name='email_test'),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # ajax view
    url(r'^ajax/', include('custom_form_app.urls', namespace="custom_form_app")),

    # upload image
    url(r'^upload_image/', include('upload_image_box.urls', namespace="upload_image_box")),
    # upload image example
    # url(r'^example_upload_image/', include('upload_image_box.example.urls', namespace="example_upload_image_box")),

    # landing pages
    url(r'^l/concorso-per-modelle/$', 'website.views.landing_landing1', name='landing_landing1'),
    url(r'^l/evento-tendenze-moda/$', 'website.views.landing_landing2', name='landing_landing2'),
    url(r'^l/beauty-and-pics/$', 'website.views.beauty_and_pics', name='beauty_and_pics'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL_TMP, document_root=settings.MEDIA_ROOT)
