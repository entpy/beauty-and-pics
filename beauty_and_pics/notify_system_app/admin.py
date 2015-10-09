# -*- coding: utf-8 -*-

from django.contrib import admin
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from beauty_and_pics.consts import project_constants
from notify_system_app.models import Notify
from notify_system_app.models import User_Notify
from notify_system_app.forms import NotifyForm
from account_app.models.accounts import Account
import sys, logging

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class NotifyAdmin(admin.ModelAdmin):
    """
    class Media:
        js = ('notify_system_app/js/test.js',)
    """

# admin custom view {{{
# require AdminPlus -> https://github.com/jsocol/django-adminplus
def create_webpush(request, *args, **kwargs):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NotifyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL with success message:
            if request.POST.get('send_via_email'):
                messages.add_message(request, messages.SUCCESS, 'La notifica è stata creata con successo, seleziona i destinatari che la riceveranno anche via email')
                return HttpResponseRedirect('/admin/send-email-notify/2')
                # return render(request, 'admin/send-email-notify.html', { 'notify_id': 2, })
            else:
                messages.add_message(request, messages.SUCCESS, 'La notifica è stata creata con successo')
                return HttpResponseRedirect('/admin/create-webpush')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NotifyForm()

    context = {
            'title' : 'Crea una notifica webpush',
            'app_name' : 'notify_system_app',
            'adminform' : form,
    }

    return render(request, 'admin/create_webpush.html', context)

def send_email_notify(request, *args, **kwargs):
    notify_obj = Notify()
    notify_retrieved = {}
    # clear checked user session
    if not request.method == 'POST':
	request.session['checked_users'] = {}

    # show paginator
    contact_list = Account.objects.filter(user__groups__name=project_constants.CATWALK_GROUP_NAME)
    paginator = Paginator(contact_list, 10) # Show 25 contacts per page
    checked_contacts = None

    # save checked elements into session
    request.session['checked_users'] = notify_obj.save_checked_elemets(paginator=paginator, request=request)

    # retrieving all checked checkbox
    campaign_contacts_list = notify_obj.get_account_list(request=request)

    # if this is a POST request we need to process the form data
    # convertito in intero perche la request è in unicode u'
    # e il controllo non avrebbe funzionato senza conversione:
    # u'0 o u'1 risultano veri entrambi
    if request.method == 'POST' and int(request.POST.get('validate_notify_details')):
	# create a form instance and populate it with data from the request:
	form = NotifyForm(request.POST)
	# check whether it's valid:
	if form.is_valid():
            # create recipients list
            recipients_list = notify_obj.create_recipients_list(retrieve_all_users=int(request.POST.get('send_all_recipients', 0)), campaign_contacts_list=campaign_contacts_list, addictional_email_string=str(request.POST.get('addictional_recipients_emails')))
            logger.debug("### elenco destinatari: " + str(recipients_list))

            # send notify email with custom email template object app ;)
            notify_obj.send_notify_via_mail(notify_data=request.POST, recipients_list=recipients_list)

	    # redirect to a new URL with success message:
	    messages.add_message(request, messages.SUCCESS, 'La notifica è stata inviata con successo')
	    return HttpResponseRedirect('/admin/send-email-notify')

    # if a GET (or any other method) we'll create a blank form
    else:
        # create initial form value
        initial_value = notify_obj.build_form_initial_value(request=request, kwargs=kwargs)
        form = NotifyForm(initial=initial_value)

    # retrieving new page number
    if (request.POST.get('next', '')):
            page = request.POST.get('next_page')
    else:
            page = request.POST.get('previously_page')

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    context = {
            'title': 'Invia una notifica via email',
            'app_name': 'notify_system_app',
            'adminform': form,
            'campaign_contacts_list': campaign_contacts_list,
            'notify_id': kwargs['notify_id'] or '',
            'contacts': contacts,
            'checked_contacts': checked_contacts,
    }

    return render(request, 'admin/send-email-notify.html', context)
# admin custom view }}}

admin.site.register(Notify, NotifyAdmin)
admin.site.register(User_Notify)
admin.site.register_view('create-webpush', 'Create webpush', view=create_webpush)
admin.site.register_view('send-email-notify/(?:(?P<notify_id>.+)/)?', 'Send email notify', view=send_email_notify)

"""
Creazione notifiche:
 - Form per l'inserimento della webpush
 - Sezione per inviare notifiche via mail a determinati utenti
 - Per inviare le webpush anche via mail, arrivare in pagina con l'id webpush
   e precompilare il form.

Visualizzazione sulla piattaforma:
 - messaggio di alert alla nuova notifica webpush
 - pagina per visualizzare le notifiche ordinate per data, a blocchi di 'n'
   e se lette o no
 - pagina dettaglio notifica con il contenuto della webpush
"""
