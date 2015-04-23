# -*- coding: utf-8 -*-

from django import forms
from account_app.models import *
from custom_form_app.forms.base_form_class import *
from upload_image_box.widgets import UibUploaderInput
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class profileImageForm(forms.Form, FormCommonUtils):
    # custom upload button template
    custom_upload_button = '<div style="background-color: cyan; display: inline-block; text-align: center; cursor: pointer; color: #666; padding: 10px; margin: 10px; width: 200px; border-radius: 5px;" data-widget-id="%(widget_id)s" class="uploaderButtonClickAction">%(widget_button_text)s</div>'
    # form fields
    uploaded_image = forms.CharField(widget=UibUploaderInput(attrs={'widget_id': 'uploader_no_crop', "enable_crop": True, "widget_button_text": "Crop load", "crop_modal_description_text": "Seleziona la porzione dell'immagine per il tuo profilo", "default_uploader_button": custom_upload_button, 'callback_function': 'saveProfileImage'}))
    image_id = forms.CharField(widget=forms.HiddenInput())
    image_type = forms.CharField(widget=forms.HiddenInput())

class bookImagesForm(forms.Form, FormCommonUtils):
    # custom upload button template
    custom_upload_button = '<div style="background-color: cyan; display: inline-block; text-align: center; cursor: pointer; color: #666; padding: 10px; margin: 10px; width: 200px; border-radius: 5px;" data-widget-id="%(widget_id)s" class="uploaderButtonClickAction">%(widget_button_text)s</div>'
    # form fields
    uploaded_image = forms.CharField(widget=UibUploaderInput(attrs={'widget_id': 'uploader_crop', "enable_crop": "", "widget_button_text": "No crop load", "crop_modal_description_text": "Seleziona la porzione dell'immagine per il tuo profilo", 'callback_function': 'saveBookImage'}))
    image_id = forms.CharField(widget=forms.HiddenInput())
    image_type = forms.CharField(widget=forms.HiddenInput())
