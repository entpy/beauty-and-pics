from django.shortcuts import render
from django.http import HttpResponse
from custom_form_app.forms.register_form import *
from custom_form_app.forms.password_recovery import *
from custom_form_app.forms.account_edit_form import *
import logging, json

# Get an instance of a logger
logger = logging.getLogger('django.request')

def validate_form(request):
    """ View to validate a form via AJAX """
    # logger.debug("chiamata ajax")
    json_response = json.dumps('{ "error": True }')

    form_class = request.POST.get("form_class", "")

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
	exec("form = " + form_class + "(request.POST)")
        # check if form is valid
        form.is_valid()
        json_response = form.get_validation_json_response()

    # return validation via ajax
    return HttpResponse(json_response, content_type="application/json")

def manage_form(request):
    """ View to data via AJAX """
    # logger.debug("chiamata ajax")

    form_class = request.POST.get("form_class", "")

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
	exec("form = " + form_class + "(request.POST)")
        # check whether it's valid:
        if form.is_valid():
		# saving data inside model
                form.actions()

    # return json data
    return HttpResponse(form.get_validation_json_response(), content_type="application/json")
