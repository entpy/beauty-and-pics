# -*- coding: utf-8 -*-

from django.shortcuts import render
from upload_image_box.forms import uploadedImagesForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def upload(request):
    # TODO: this must return an image path after image upload
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
