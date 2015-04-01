from django.db import models
from django.contrib.auth.models import User
from ajaximage.fields import AjaxImageField

class Image(models.Model):
    id_image = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    # image_url = models.ImageField(upload_to='book_img/')
    image_url = AjaxImageField(upload_to='book_img/')
    image_type = models.IntegerField()

    class Meta:
        app_label = 'account_app'

"""
	* id_image (PK)
	* user (FK)
	* image_url
	* image_type (0 foto profilo, 1 foto del book)
"""
