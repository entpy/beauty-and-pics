# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.core.files import File
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy

class UibUploaderInput(forms.ClearableFileInput):

    def __init__(self, attrs=None):
        # qui dovrei passare delle opzioni al plugin, per esempio un qualcosa
        # che abiliti/disabiliti la funzionalità di crop o che ne definisca i
        # dettagli (es. area di crop fissa, ecc...)
        super(UibUploaderInput , self).__init__(attrs=None)
        initial_text = ugettext_lazy('Currently')
        input_text = ugettext_lazy('Change')
        clear_checkbox_label = ugettext_lazy('Clear')

        template_with_initial = (
            '%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> '
            '%(clear_template)s<br />%(input_text)s: %(input)s'
        )

        template_with_clear = '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    # metodo per scrivere nell'html il file input
    # questa funzione viene eseguita al rendering dell'html
    #def render(self, name, value, attrs=None):
    #    return = super(UibUploaderInput, self).render(name, value, attrs)
    """
    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(UibUploaderInput, self).render(name, value, attrs)

        ""
        if self.is_initial(value):
            template = self.template_with_initial
            substitutions.update(self.get_template_substitution_values(value))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions
        ""

        return mark_safe(template % substitutions)
    """

    """
    def value_from_datadict(self, data, files, name):
    """

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
