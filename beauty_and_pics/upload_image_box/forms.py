# -*- coding: utf-8 -*-

from django.forms import ModelForm
from upload_image_box.models import uploadedImages
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class uploadedImagesForm(ModelForm):
    class Meta:
        model = uploadedImages
	fields = ("__all__")
