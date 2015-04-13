# -*- coding: utf-8 -*-

from django.db import models

class uploadedImages(models.Model):
    image = models.ImageField(upload_to='upload_image_box/') 
    upload_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.image
