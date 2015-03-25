from django.shortcuts import render
from django.http import HttpResponse
from custom_form_app.ajax_manager import ajaxManager
import logging, json

# Get an instance of a logger
logger = logging.getLogger(__name__)

def ajax_action(request):
    """ View to perform an action as function via javascript aka AJAX call"""

    # load and perform action
    ajaxManager_obj = ajaxManager(request=request)
    ajaxManager_obj.perform_ajax_action()
    json_response = ajaxManager_obj.get_json_response()

    # return a JSON response
    return HttpResponse(json_response, content_type="application/json")
