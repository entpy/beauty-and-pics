"""
Django settings for upload_image_box project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

APP_BASE_DIRECTORY = 'upload_image_box/'
UPLOADED_IMG_TMP_DIRECTORY = 'tmp_upload/'
CROPPED_IMG_MIN_WIDTH = 200
CROPPED_IMG_MIN_HEIGHT = 200

# TODO
"""
TODO
====

Capire dove e come inserire i seguenti parametri del plugin:
i testi (dei pulsanti e dei titoli)
la larghezza/altezza minima dell'immagine uploadata
la larghezza/altezza minima dell'immagine croppata
se abilitare o no il crop dell'immagine (saltare alla pagina di riepilogo o mostrare il crop)
l'html del widget
"""
