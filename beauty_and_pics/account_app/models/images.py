# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.templatetags.static import static
from upload_image_box.models import cropUploadedImages 
from website.exceptions import *
from beauty_and_pics.consts import project_constants
import logging, datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Book(models.Model):
    # book_id = models.IntegerField(primary_key=True)
    image_id = models.OneToOneField(cropUploadedImages, primary_key=True)
    user = models.ForeignKey(User)
    image_type = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'account_app'

    def __unicode__(self):
        return self.image_id.image.url

    # TODO: save an uploaded image:
    #       - se questo image_id non è associato ancora a nessun utente lo
    #       salvo, altrimenti il dato è stato modificato da terzi e lo scarto
    #       (non faccio nessun inserimento)
    #       - return saved image url
    def save_book_image(self, image_data):
        """Function to save a new image (profile image or book image)"""
        return_var = None
        if image_data:
	    try:
                book_obj = Book()
                book_obj.image_id = self.get_crop_uploaded_image_obj(image_id=image_data["image_id"])
	    except croppedImageDoesNotExistError:
	        raise
            else:
                book_obj.user = image_data["user"]
                book_obj.image_type = image_data["image_type"]
                book_obj.save()
                return_var = book_obj

        return return_var

    def delete_book_image(self, image_id=None, user_id=None):
        """Function to delete an image (profile image or book image)"""
        return_var = None
        if image_id and user_id:
            try:
                # retrieve image
                book_image = Book.objects.get(pk=image_id)
            except Book.DoesNotExist:
                raise bookImageDoesNotExistError
            else:
                if user_id == book_image.user.id:
                    # if the user_id of the image match with session user id, the
                    # image can be deleted
                    logger.debug("<<image can be deleted>>")
                    try:
                        cropped_image = self.get_crop_uploaded_image_obj(image_id=image_id)
                    except cropUploadedImages.DoesNotExist:
                        raise croppedImageDoesNotExistError
                    else:
                        # delete row from crop table (this delete also row in book
                        # tables) and related thumb image and full image
                        logger.debug("DELETE book image -> user_id: " + str(user_id) + " | book_image_user_id: " + str(book_image.user.id))
                        cropped_image.delete()
                        return_var = True
                else:
                    raise deleteImageReferenceError

        return return_var

    def get_crop_uploaded_image_obj(self, image_id):
        """Function to retrieve crop uploaded image instance"""
        return_var = None
	try:
	    return_var = cropUploadedImages.objects.get(pk=image_id)
            logger.debug("cropped img: " + str(return_var))
	except cropUploadedImages.DoesNotExist:
            raise croppedImageDoesNotExistError

        return return_var

    def check_image_type_exists(self, image_type):
        """Function to check if an image type exists"""
	if image_type not in ['profile_image', 'book_image']:
	    raise imageTypeWrongError

        return True

    def get_photobook_list(self, user_id, filters_list=None):
        """Function to retrieve a list of photobook about a user"""
        return_var = False
        page_load_datetime = False
        if filters_list.get("page_loaded_timestamp"):
            page_load_datetime = datetime.datetime.fromtimestamp(float(filters_list["page_loaded_timestamp"]))
        if user_id:
            if page_load_datetime:
                return_var = Book.objects.values('image_id__id', 'image_id__thumbnail_image__image', 'image_id__image').filter(user__id=user_id, image_type=project_constants.IMAGE_TYPE["book"], upload_date__lte=page_load_datetime)
            else:
                return_var = Book.objects.values('image_id__id', 'image_id__thumbnail_image__image', 'image_id__image').filter(user__id=user_id, image_type=project_constants.IMAGE_TYPE["book"])
            # list orders
            return_var = return_var.order_by('-image_id__id')
            # list limits
            return_var = list(return_var[filters_list["start_limit"]:filters_list["show_limit"]])

        return return_var

    def get_all_photobook_list(self, contest_type, filters_list=None):
        """
            Function to retrieve a list of photobook about all users ordered by date
            prelevo solo le foto degli utenti che appartengono al gruppo "catwalker"
            e che hanno flag can_be_shown=1
        """
	from account_app.models import Account
	Account_obj = Account()

	# retrieve all photos about a contest_type
	return_var = Book.objects.values('user__id', 'image_id__thumbnail_image').filter(user__account__contest_type__code=contest_type, image_type=project_constants.IMAGE_TYPE["book"])
	# apply default account filters
	return_var = Account_obj.apply_catwalker_filters(contest_type=contest_type, queryset=return_var)
	# list orders
	return_var = return_var.order_by('-upload_date')
	# list limits
	if filters_list.get("start_limit") or filters_list.get("show_limit"):
	    return_var = return_var[filters_list["start_limit"]:filters_list["show_limit"]]

        return list(return_var)

    def get_profile_image(self, user_id, thumbnail=False):
        """Function to retrieve profile image, if exists more profile image than take only last"""
        return_var = None
	if user_id:
            if thumbnail:
                return_var = Book.objects.values('image_id__id', 'image_id__thumbnail_image__image').filter(user__id=user_id, image_type=project_constants.IMAGE_TYPE["profile"])
            else:
                return_var = Book.objects.values('image_id__id', 'image_id__image').filter(user__id=user_id, image_type=project_constants.IMAGE_TYPE["profile"])
            return_var = return_var.order_by('-image_id__id')
            if (return_var):
                return_var = return_var[0]

        return return_var

    def get_profile_image_url(self, user_id, return_default=True):
        """Function to retrieve profile image url"""
        return_var = None
        profile_image = self.get_profile_image(user_id=user_id)
	if profile_image and profile_image["image_id__image"]:
            return_var = self.get_base_image_url() + profile_image["image_id__image"]

        # default profile image
        if not return_var and return_default:
            return_var = static('website/img/catwalk/default_profile_image.jpg')

        return return_var

    def get_profile_thumbnail_image_url(self, user_id, return_default=True):
        """Function to retrieve profile image url"""
        return_var = None
        profile_image = self.get_profile_image(user_id=user_id, thumbnail=True)
	if profile_image and profile_image["image_id__thumbnail_image__image"]:
            return_var = self.get_base_image_url() + profile_image["image_id__thumbnail_image__image"]

        # default profile image
        if not return_var and return_default:
            return_var = static('website/img/catwalk/default_profile_image.jpg')

        return return_var

    def get_image_url(self, book_image_id):
        """Function to retrieve and image url from image id"""
	logger.debug("id immagine: " + str(book_image_id))
	return_var = None
	try:
	    image_obj = cropUploadedImages.objects.values('image').get(pk=book_image_id)
	    logger.debug("immagine trovata")
	except cropUploadedImages.DoesNotExist:
	    logger.debug("immagine NON trovata")
	    # image not found
	    pass
        else:
            return_var = str(image_obj['image'])

        return return_var

    def exists_user_images(self, user_id):
        """Function to count images about a user"""
        return_var = 0
        page_load_datetime = False
        if user_id:
	    return_var = Book.objects.filter(user__id=user_id, image_type=project_constants.IMAGE_TYPE["book"]).exists()

        return return_var

    def get_base_image_url(self):
	"""Function to retrieve base image url: http:www.hostimage.com/image_folder/"""
	return settings.MEDIA_URL

"""
	* id_image (PK)
	* user (FK)
	* image_url
	* image_type (0 foto profilo, 1 foto del book)
"""
