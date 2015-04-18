# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.http import require_POST
from upload_image_box.forms import uploadedImagesForm
from upload_image_box.models import uploadedImages
from django.conf import settings
from .settings import *
from django.http import HttpResponse
import logging, json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# View to upload an image
@require_POST
def upload(request):
    data = {'error' : True}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = uploadedImagesForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            image_form = form.save(commit=False)
            image_form.upload_to = UPLOADED_IMG_TMP_DIRECTORY
            image_form.save()
            # file_path = save_file(file=request.FILES['image'], path="tmp_upload/")
            data = {'success' : True, "file_id": image_form.id, "file_url": "http://" + str(request.get_host()) + str(settings.MEDIA_URL) + str(image_form.image)}
            # logger.debug("immagine salvata: " + str(settings.MEDIA_URL) + str(image_form.image))
        else:
            logger.debug("form NON valido: " + str(form.errors))
	    pass

    return HttpResponse(json.dumps(data), content_type="application/json")

# View to crop an uploaded image
@require_POST
def crop(request):
    data = {'error' : True}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
	try:
	    uploaded_mages_obj = uploadedImages()
            # retrieve crop info
	    crop_info = uploaded_mages_obj.retrieve_crop_info(request)
            # load uploaded image instance
	    uploaded_image = uploadedImages.objects.get(pk=crop_info["file_id"]) # BAD
	    return_var = True
	except uploadedImages.DoesNotExist:
            data = {'error' : True, "msg": "Uploaded image doesn't exists"}
	    pass
        else:
            # crop uploaded image
	    if uploaded_mages_obj.crop_image(uploaded_image, crop_info):
		# change 'is_temp_image' flag to '0'
		uploaded_image.is_temp_image = 0
		uploaded_image.save()
		data = {'success' : True}
	    else:
	        data = {'error' : True, "msg": "Please check your crop selection!"}

    return HttpResponse(json.dumps(data), content_type="application/json")

# Example view
def upload_example(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = uploadedImagesForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
	    form.save()
        else:
            logger.debug("form NON valido: " + str(form.errors))
	    pass

    # if a GET (or any other method) we'll create a blank form
    else:
        form = uploadedImagesForm()

    context = {
        "post" : request.POST,
        "form": form,
    }

    return render(request, 'upload_image_box/upload_example.html', context)
