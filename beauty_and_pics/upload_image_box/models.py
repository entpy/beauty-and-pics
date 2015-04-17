# -*- coding: utf-8 -*-

from django.db import models
from .settings import *
import os

def get_image_path(self, filename):
    return os.path.join(self.upload_to_base_path, self.upload_to, filename)

class uploadedImages(models.Model):
    image = models.ImageField(max_length=500, upload_to=get_image_path)
    upload_date = models.DateTimeField(auto_now=True)
    is_temp_image = models.IntegerField(null=True, default=1)

    # upload file attributes
    upload_to_base_path = APP_BASE_DIRECTORY # default file upload base dir
    upload_to = '' # default file upload custom dir

    def __unicode__(self):
        return self.image
