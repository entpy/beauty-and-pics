# -*- coding: utf-8 -*-

from django.forms import ModelForm
from upload_image_box.models import tmpUploadedImages, cropUploadedImages
from upload_image_box.widgets import UibUploaderInput
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class uploadedImagesNoCropForm(ModelForm):
    class Meta:
        model = tmpUploadedImages
	fields = ("image",)
        widgets = {
            'image': UibUploaderInput(attrs={'widget_id': 'uploader_no_crop', 'custom_upload_dir_name': "", "enable_crop": "", "upload_modal_title_text": "Attendi mentre carichiamo l'immagine..."}),
        }

class uploadedImagesCropForm(ModelForm):
    class Meta:
        model = tmpUploadedImages
	fields = ("image",)
        widgets = {
            'image': UibUploaderInput(attrs={'widget_id': 'uploader_crop', 'custom_upload_dir_name': "", "enable_crop": True, "upload_modal_title_text": "Attendi mentre carichiamo l'immagine..."}),
        }
