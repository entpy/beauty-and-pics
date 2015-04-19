# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.core.files import File
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy
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
    template_with_initial = '%(uploader_button)s%(modal_window_scheleton)s%(uploader_script)s%(uploader_options)s'
            
    def __init__(self, attrs=None):
        # TODO qui dovrei passare delle opzioni al plugin, per esempio un qualcosa
        # che abiliti/disabiliti la funzionalità di crop o che ne definisca i
        # dettagli (es. area di crop fissa, ecc...)
        # default_attrs = {'cols': '40', 'rows': '10'}
        # if attrs:
            # default_attrs.update(attrs)
        self.uploader_button = '<div class="uploader_button uploaderButtonClickAction">Click me!</div>'
        self.modal_window_scheleton = '<div class="modal_container"></div>'
        self.uploader_script = '<script type="text/javascript">$(function(){uploaderImageBox.init();});</script>'
        self.uploader_options = '<div class="uploader_image_box_options" data-custom-upload-dir-name="blu" style="display: none!important"></div>'
        super(UibUploaderInput , self).__init__(attrs=None)

    # metodo per scrivere nell'html il file input
    # questa funzione viene eseguita al rendering dell'html
    def render(self, name, value, attrs=None):
        substitutions = {
            'uploader_button': self.uploader_button,
            'modal_window_scheleton': self.modal_window_scheleton,
            'uploader_script': self.uploader_script,
            'uploader_options': self.uploader_options,
        }
        template = self.template_with_initial

        return mark_safe(template % substitutions)

    def value_from_datadict(self, data, files, name):
        # if a file was uploaded
        file = super(UibUploaderInput, self).value_from_datadict(data, files, name)
        # logger.debug("parent file: " + str(file))
        if file is not None:  # super class may return a file object, False, or None
            return file  # Default behaviour
        return None

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
