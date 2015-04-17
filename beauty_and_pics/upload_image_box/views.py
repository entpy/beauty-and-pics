# -*- coding: utf-8 -*-

from django.shortcuts import render
from upload_image_box.forms import uploadedImagesForm
from upload_image_box.models import uploadedImages
from django.conf import settings
from .settings import *
from django.http import HttpResponse
from PIL import Image
import os, logging, json

# Get an instance of a logger
logger = logging.getLogger(__name__)

def upload(request):
    data = {'error' : True, }
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = uploadedImagesForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            image_form = form.save(commit=False)
            image_form.upload_to = 'tmp_upload/'
            image_form.save()
            # file_path = save_file(file=request.FILES['image'], path="tmp_upload/")
            data = {'success' : True, "file_id": image_form.id, "file_url": "http://" + str(request.get_host()) + str(settings.MEDIA_URL) + str(image_form.image)}
            logger.debug("immagine salvata: " + str(settings.MEDIA_URL) + str(image_form.image))
        else:
            logger.debug("form NON valido: " + str(form.errors))

    return HttpResponse(json.dumps(data), content_type="application/json")

def crop(request):
    logger.debug("=== crop info START ===")
    logger.debug("file_id: " + str(request.POST.get("file_id")))
    logger.debug("height: " + str(request.POST.get("height")))
    logger.debug("width: " + str(request.POST.get("width")))
    logger.debug("x: " + str(request.POST.get("x")))
    logger.debug("y: " + str(request.POST.get("y")))
    logger.debug("rotate" + str(request.POST.get("rotate")))
    logger.debug("=== crop info END ===")
    data = {'error' : True, }
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        file_id = request.POST.get("file_id")
        height = int(str(request.POST.get("height")))
        width = int(str(request.POST.get("width")))
        x = int(str(request.POST.get("x")))
        y = int(str(request.POST.get("y")))
        rotate = request.POST.get("rotate")
        # use PIL to resize and save new image
        # create a form instance and populate it with data from the request:
	try:
	    uploaded_image = uploadedImages.objects.get(pk=file_id)
	    return_var = True
	except uploadedImages.DoesNotExist:
            # plz manage this exception
	    pass
        else:
            # TODO: crop uploaded image
	    image_path = settings.MEDIA_ROOT + "/" + str(uploaded_image.image)
            logger.debug("opening image: " + str(image_path))
	    image = Image.open(image_path)
	    width, height = image.size   # Get dimensions
            logger.debug("width: " + str(width) + " | height: " + str(height))
	    image.crop([x, y, width, height])
	    image.save(image_path)

	    # controllare i valori del crop che danno errori strani tipo -> invalid literal for int() with base 10: '345.8'
            # TODO: change 'is_temp_image' flag to '0'
            # TODO: move image to another directory

    return HttpResponse(json.dumps(data), content_type="application/json")

def upload_example(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = uploadedImagesForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            logger.debug("file upload to save: " + str(request.FILES))
	    form.save()
        else:
            logger.debug("form NON valido: " + str(form.errors))
	    # success redirect to catwalk

    # if a GET (or any other method) we'll create a blank form
    else:
        form = uploadedImagesForm()

    context = {
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'upload_image_box/upload_example.html', context)
