from django.shortcuts import render
from django.http import HttpResponse
from custom_form_app.forms.register_form import *
from account_app.models import *
import logging, json

# Get an instance of a logger
logger = logging.getLogger('django.request')

def manage_form(request):
    # logger.debug("chiamata ajax")

    form_class = request.POST.get("form_class", "")

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
	exec("form = " + form_class + "(request.POST)")
        # check whether it's valid:
        if form.is_valid():
		# saving data inside model
                form.save(models = {"Account" : Account()})

    # return json data
    return HttpResponse(form.get_validation_json_response(), content_type="application/json")
