from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    id_image = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    # image_url = models.ImageField(upload_to='book_img/')
    image_url = models.ImageField(upload_to='book_img/')
    image_type = models.IntegerField()

    class Meta:
        app_label = 'account_app'

"""
	* id_image (PK)
	* user (FK)
	* image_url
	* image_type (0 foto profilo, 1 foto del book)
"""

# 1 pulsante per aprire popup "upload image"
# 2 all'interno del popup un ulteriore pulsante per upload immagine
# 3 alla selezione dell'immagine ricaricare l'iframe con l'immagine uploadata
#   e il crop di proporzioni fisse
# 4 ora è possibile fare due cose: modificare l'immagine uploadata con
#   un'altra (si riparte dallo step 3), oppure confermare il crop
# 5 alla conferma del crop salvare l'immagine croppata su disco, meglio ancora se su S3
# come fare tutto ciò come un Django widget? :o
