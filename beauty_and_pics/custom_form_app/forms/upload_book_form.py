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
    custom_upload_button = '<div data-widget-id="%(widget_id)s" class="uploaderButtonClickAction upload_profile_image_button btn btn-success">%(widget_button_text)s</div>'
    # form fields
    widget_attr = {
            'widget_id': 'uploader_1',
            'enable_crop': True,
            'default_uploader_button': custom_upload_button,
            'callback_function': 'saveProfileImage',
            'base_modal_title_text': "Seleziona un'immagine",
            'upload_modal_title_text': 'Caricamento in corso, attendi...',
            'crop_modal_title_text': 'Seleziona area immagine',
            'preview_modal_title_text': 'Anteprima immagine',
            'crop_action_button_text': 'Conferma immagine',
            'select_image_action_button_text': 'Seleziona immagine',
            'widget_button_text': 'Carica immagine',
            'preview_action_button_text': 'Conferma immagine',
            'cancel_button_text': 'Chiudi',
            'change_image_button_text': 'Cambia immagine',
            'crop_modal_description_text': "Seleziona la porzione dell'immagine per il tuo profilo",
    }
    uploaded_image = forms.CharField(widget=UibUploaderInput(attrs=widget_attr))
    image_id = forms.CharField(widget=forms.HiddenInput())
    image_type = forms.CharField(widget=forms.HiddenInput())

class bookImagesForm(forms.Form, FormCommonUtils):
    # custom upload button template
    custom_upload_button = '<div data-widget-id="%(widget_id)s" class="uploaderButtonClickAction upload_book_image_button btn btn-success">%(widget_button_text)s</div>'
    # form fields
    widget_attr = {
            'widget_id': "uploader_2",
            'enable_crop': True,
            'default_uploader_button': custom_upload_button,
            'callback_function': "saveBookImage",
            'base_modal_title_text': "Seleziona un'immagine",
            'upload_modal_title_text': 'Caricamento in corso, attendi...',
            'crop_modal_title_text': 'Seleziona area immagine',
            'preview_modal_title_text': 'Anteprima immagine',
            'crop_action_button_text': 'Conferma immagine',
            'select_image_action_button_text': 'Seleziona immagine',
            'widget_button_text': 'Aggiungi immagine +',
            'preview_action_button_text': 'Conferma immagine',
            'cancel_button_text': 'Chiudi',
            'change_image_button_text': 'Cambia immagine',
            'crop_modal_description_text': "Seleziona la porzione dell'immagine per il tuo book",
    }
    uploaded_image = forms.CharField(widget=UibUploaderInput(attrs=widget_attr))
    image_id = forms.CharField(widget=forms.HiddenInput())
    image_type = forms.CharField(widget=forms.HiddenInput())
