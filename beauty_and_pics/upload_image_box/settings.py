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
CROPPED_IMG_DIRECTORY = 'cropped_upload/'
CUSTOM_CROPPED_IMG_DIRECTORY = '' # ex. "user_12/"
CROPPED_IMG_MIN_WIDTH = 200
CROPPED_IMG_MIN_HEIGHT = 200

# TODO
"""
TODO
====

- V Spostare le immagini croppate nella directory CROPPED_IMG_DIRECTORY

- Eliminare le immagini nella cartella UPLOADED_IMG_TMP_DIRECTORY e dal db temporaneo dopo un tot di tempo (capire come fare)

- Capire dove e come inserire i seguenti parametri del widget:
	V i testi (dei pulsanti e dei titoli)
	  la larghezza/altezza minima dell'immagine uploadata
	  la larghezza/altezza minima dell'immagine croppata
	V se abilitare o no il crop dell'immagine (saltare alla pagina di riepilogo o mostrare il crop)
	  l'html del widget
- Modificare $('#upload_image_box_modal') in una classe per poter utilizzare più loader nella stessa pagina

Per inserire le immagini in una directory custom inserire il nome nell'impostazione del widget e nella view 
che genera il widget per l'upload. In questo modo sono in grado di controllare che non avvengano caricamenti
in directory differenti da quelle definite (modificando il valore in javascript per esempio)
"""
