# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.core.files import File
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy
from django.core.files.images import get_image_dimensions
from upload_image_box.exceptions import *

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class UibUploaderInput(forms.ClearableFileInput):

    # override default ClearableFileInput data
    initial_text = '' # ugettext_lazy('Currently')
    input_text = '' # ugettext_lazy('Change')
    clear_checkbox_label = '' # ugettext_lazy('Clear')
    template_with_clear = '' # '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    # default template is a simple div
    template_with_initial = '%(uploader_button)s%(modal_window_scheleton)s%(uploader_script)s'

    def __init__(self, attrs=None):
        # set valid checks
        self.max_file_size = 4*1024*1024 # 4MB
        self.min_file_width = 200
        self.min_file_height = 200
        self.file_extensions_allowed = []
        # TODO qui dovrei passare delle opzioni al plugin, per esempio un qualcosa
        # che abiliti/disabiliti la funzionalità di crop o che ne definisca i
        # dettagli (es. area di crop fissa, ecc...)
	self.default_attrs = {
		'custom_upload_dir_name': '',
		'base_modal_title_text': 'Load an image',
		'upload_modal_title_text': 'Image upload...',
		'crop_modal_title_text': 'Crop your image',
		'preview_modal_title_text': 'Image preview',
		'crop_action_button_text': 'Crop',
		'select_image_action_button_text': 'Select image',
		'widget_button_text': 'Load image',
		'preview_action_button_text': 'Confirm image',
		'cancel_button_text': 'Cancel',
		'change_image_button_text': 'Change image',
                'crop_modal_description_text': "Crop your image!",
		'enable_crop': True,
                'widget_id': 'test_id', # only required field
	}

        # overriding defaul attributes
        if attrs:
            self.default_attrs.update(attrs)

        self.uploader_button = '<div data-widget-id="%(widget_id)s" class="uploader_button uploaderButtonClickAction">%(widget_button_text)s</div>' # TODO: use custom html
        self.modal_window_scheleton = '<div id="%(widget_id)s" class="modal_container" data-custom-upload-dir-name="%(custom_upload_dir_name)s" data-base-modal-title-text="%(base_modal_title_text)s" data-upload-modal-title-text="%(upload_modal_title_text)s" data-crop-modal-title-text="%(crop_modal_title_text)s" data-preview-modal-title-text="%(preview_modal_title_text)s" data-crop-action-button-text="%(crop_action_button_text)s" data-preview-action-button-text="%(preview_action_button_text)s" data-cancel-button-text="%(cancel_button_text)s" data-change-image-button-text="%(change_image_button_text)s" data-enable-crop="%(enable_crop)s" data-select-image-action-button-text="%(select_image_action_button_text)s" data-crop-modal-description-text="%(crop_modal_description_text)s"></div>'
        self.uploader_script = '<script type="text/javascript">$(function(){uploaderImageBox.init("%(widget_id)s");});</script>'
        # self.uploader_options = '<div class="' + str(self.default_attrs["widget_id"]) '_options" style="display: none!important"></div>'
        super(UibUploaderInput , self).__init__(attrs=None)

    # metodo per scrivere nell'html il file input
    # questa funzione viene eseguita al rendering dell'html
    def render(self, name, value, attrs=None):
	logger.debug("attrs list: " + str(self.default_attrs))
        substitutions = {
            'uploader_button': (self.uploader_button % self.default_attrs),
            'modal_window_scheleton': (self.modal_window_scheleton % self.default_attrs),
            'uploader_script': (self.uploader_script % self.default_attrs),
            # 'uploader_options': (self.uploader_options % self.default_attrs),
        }
        template = self.template_with_initial

        return mark_safe(template % substitutions)

    # Function to validate widget, called on form.is_valid()
    def value_from_datadict(self, data, files, name):
        # if a file was uploaded
        parent_validation = super(UibUploaderInput, self).value_from_datadict(data, files, name)
        # logger.debug("files retrieved: " + str(files))
        file_object = files.get('image', None)
        logger.debug("file object: " + str(file_object))
        if parent_validation is not None and file_object is not None:
            # retrieve image info
            file_size = file_object.size
            file_w, file_h = get_image_dimensions(file_object)
            # TODO: check image MIME/Type
            # image size check
            logger.debug("Image size: " + str(file_size) + " massima: " + str(self.max_file_size))
            if file_size > self.max_file_size:
                raise ImageSizeUIBError
            # image dimensions check
            logger.debug("Image w: " + str(file_w)+ " image h: " + str(file_h))
            if file_w < self.min_file_width or file_h < self.min_file_height:
                raise ImageDimensionsUIBError
            return file_object  # Return valid file object
        else:
            # raise corrupted file error
            raise CorruptedImageUIBError

    class Media:
        css = {
            'all': ("upload_image_box/css/widget.css",)
        }
        js = ("upload_image_box/js/widget.js",)

    # INTRO
    # =====
    #
    # 1 pulsante per aprire popup "upload image"
    # 2 all'interno del popup un ulteriore pulsante per upload immagine
    # 3 alla selezione dell'immagine ricaricare l'iframe con l'immagine uploadata
    #   e il crop di proporzioni fisse
    # 4 ora è possibile fare due cose: modificare l'immagine uploadata con
    #   un'altra (si riparte dallo step 3), oppure confermare il crop
    # 5 alla conferma del crop salvare l'immagine croppata su disco, meglio ancora se su S3
    # come fare tutto ciò come un Django widget? :o
