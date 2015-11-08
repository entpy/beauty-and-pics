# -*- coding: utf-8 -*-

from django.db import models, IntegrityError
from django.db.models import F
from django.contrib.auth.models import User
from django.utils import timezone
from contest_app.models import Contest
from upload_image_box.models import cropUploadedImages 
from image_contest_app.exceptions import *
from .settings import *
from datetime import datetime, timedelta
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ImageContest(models.Model):
    image_contest_id = models.AutoField(primary_key=True)
    contest = models.ForeignKey(Contest) # woman contest or man contest
    status = models.IntegerField(default=0) # (0 attivo per la votazione, 1 chiuso, 2 terminato => non considerarlo più)
    creation_date = models.DateTimeField(auto_now_add=True) # contest creation date
    expiring = models.DateTimeField(null=True) # contest expiring
    like_limit = models.IntegerField(null=True) # image max like

    class Meta:
        app_label = 'image_contest_app'

    def __unicode__(self):
        return str(self.image_contest_id) + " " + str(self.type) + " " + str(self.creation_date)

    def image_contest_manager(self):
        """Function to manage image contests"""
        # logger.info("image contest manager")
        # close expired image contests
        self.__terminate_expired_contests()
        # create new image contests
        self.__create_contests()

        return True

    def __terminate_expired_contests(self):
        """
        itero su tutti i concorsi chiusi (status=1)
            se la data corrente è >= della scadenza
                - termino il concorso (settando lo status=2  |1 -> 2|)
                - salvo tutto in ImageContestHallOfFame
        """
        image_contest_list = ImageContest.objects.filter(status=ICA_CONTEST_TYPE_CLOSED, expiring__lte=timezone.now())
        for image_contest in image_contest_list:
            # TODO: save into ImageContestHallOfFame
            pass

        ImageContest.objects.filter(status=ICA_CONTEST_TYPE_CLOSED, expiring__lte=timezone.now()).update(status=ICA_CONTEST_TYPE_FINISHED)

        return True

    def __create_contests(self):
        # creo i nuovi image contest, uno per il man contest e l'altro per il woman contest
        """
        Itero sui concorsi attivi (per ora "uomo" e "donna")
            Se per ogni tipo non esiste il concorso attivo o in fase di
            apertura (con concorso.status!=0 o concorso.status=1)
                - creo il concorso, ponendo come start_date "+ 1 mese" a partire dalla data attuale
                  e mettendo lo status a 0 (default)
        """
        Contest_obj = Contest()
        active_contests_list = Contest_obj.get_all_active_contests()
        for active_contests in active_contests_list:
            if not ImageContest.objects.filter(contest=active_contests, status=ICA_CONTEST_TYPE_ACTIVE).exists():
                # no active image contests, must be create a new one
                ImageContest_obj = ImageContest(
                    contest = active_contests,
                    like_limit = ICA_LIKE_LIMIT,
                )
                ImageContest_obj.save()
                logger.info("image contest creato")

        return True

    def get_image_contest_about_user(self, user_obj=None):
        """Function to retrieve image_contest about user_obj"""
        return_var = None
        try:
            ImageContest_obj = ImageContest.objects.get(contest__contest_type_id=user_obj.account.contest_type, status=ICA_CONTEST_TYPE_ACTIVE)
        except ImageContest.DoesNotExist:
            pass
        else:
            return_var = ImageContest_obj

        return return_var

class ImageContestImage(models.Model):
    image_contest_image_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User) # related user
    image_contest = models.ForeignKey(ImageContest) # related image contest
    image = models.ForeignKey(cropUploadedImages) # user image path
    like = models.IntegerField(default=0) # image's like
    visits = models.IntegerField(default=0) # image's visits
    creation_date = models.DateTimeField(auto_now_add=True) # image creation date

    class Meta:
        app_label = 'image_contest_app'
        unique_together = (("user", "image_contest", "image"),)

    def __unicode__(self):
        return str(self.image_contest_image_id) + " " + str(self.image.image.url)

    def add_contest_image(self, data):
        """Function to add image_contest_image element"""
        return_var = False
        """
        data = {'user_obj', 'image_user_contest_obj', 'image_obj',}
        """
        if not data.get('user_obj') or not data.get('image_user_contest_obj') or not data.get('image_obj'):
            # raise an exception
            raise AddImageContestImageFieldMissignError

        ImageContestImage_obj = ImageContestImage(
            user = data.get('user_obj'), # related user obj
            image_contest = data.get('image_user_contest_obj'), # related image contest obj
            image = data.get('image_obj'), # image obj
        )

        try:
            # try saving object
            ImageContestImage_obj.save()
        except IntegrityError:
            raise AddImageContestIntegrityError
        else:
            return_var = ImageContestImage_obj

        return return_var

    def remove_contest_image(self, image_contest_image_id, user_id):
        """Function to remove image_contest_image_id about user_id"""
        return_var = False
        try:
            ImageContestImage_obj = ImageContestImage.objects.get(image_contest_image_id=image_contest_image_id, user__id=user_id)
        except ImageContestImage.DoesNotExist:
            raise RemoveImageContestImageError
        else:
            logger.debug("DELETE ImageContestImage -> id: " + str(ImageContestImage_obj.image_contest_image_id) + " | email: " + str(ImageContestImage_obj.user.email))
            ImageContestImage_obj.delete()
            return_var = True

        return return_var

    def get_image_contest_image_obj(self, image_contest_image_id):
        """Function to retrieve image_contest_image from id"""
        return_var = False
        try:
            logger.debug("image contest image retrieve obj about id: " + str(image_contest_image_id))
            ImageContestImage_obj = ImageContestImage.objects.get(image_contest_image_id=image_contest_image_id)
        except ImageContestImage.DoesNotExist:
            raise
        else:
            return_var = ImageContestImage_obj

        return return_var

    def image_exists(self,  user_id):
        """Function to check if an image about user_id already exists"""
        return_var = False

        if ImageContestImage.objects.filter(user__id=user_id).exists():
            return_var = True

        return return_var

    def add_image_like(self, image_contest_image_id, like=1):
        """Function to add a like (+1) to an image"""
        ImageContestImage.objects.filter(image_contest_image_id=image_contest_image_id).update(like=F('like') + like)

        return True

    def add_image_visit(self, image_contest_image_id):
        """Function to add a visit to an image"""
        ImageContestImage.objects.filter(image_contest_image_id=image_contest_image_id).update(visits=F('visits') + 1)

        return True

    # TODO
    def trigger_like_limit_reach(self, image_contest_image_id):
        """
	action performed when like limit is reached:
	Function to close related image_contest and set an expiring date (now + 2 weeks)
        """
        ImageContestImage.objects.filter(image_contest_image_id=image_contest_image_id).update(image_contest__status=ICA_CONTEST_TYPE_CLOSED, image_contest__expiring=(datetime.now() + timedelta(days=14)))

        return True

    def check_like_limit(self, image_contest_image_like):
        """Function to check if like limit is reached"""
        return_var = False
        if int(image_contest_image_like) >= int(ICA_LIKE_LIMIT):
            return_var = True

        return return_var

    def get_user_contest_image_obj(self, user_id):
        """Function to retrieve contest_image_obj about user_id"""
        return_var = None
        try:
            ImageContestImage_obj = ImageContestImage.objects.get(user__id=user_id)
        except ImageContestImage.DoesNotExist:
            raise
        else:
            return_var = ImageContestImage_obj

        return return_var

    def get_user_contest_image_info(self, user_id):
        """Function to retrieve contest image info about user_id"""
        return_var = None
	user_image_contest_like_perc = 0
        try:
            ImageContestImage_obj = self.get_user_contest_image_obj(user_id)
        except ImageContestImage.DoesNotExist:
            raise
        else:
            if ImageContestImage_obj.like:
                # calculating image contest like percentage
                user_image_contest_like_perc =  100 / (int(ICA_LIKE_LIMIT) / (ImageContestImage_obj.like * 1.0))

            return_var = {
                "user_image_contest_obj" : ImageContestImage_obj,
                "user_image_contest_id" : ImageContestImage_obj.image_contest_image_id,
                "user_image_contest_url" : ImageContestImage_obj.image.image.url,
                "user_image_contest_like" : ImageContestImage_obj.like,
                "user_image_contest_like_perc" : user_image_contest_like_perc,
                "user_image_contest_visits" : ImageContestImage_obj.visits,
                "like_limit" : ICA_LIKE_LIMIT,
                "user_image_contest_like_remaining" : int(ICA_LIKE_LIMIT) - int(ImageContestImage_obj.like),
            }

        return return_var

    def show_contest_all_images(self, contest_type, filters_list=None):
        """
        ex. -> current_contest = woman_contest
        select images where image_contest.image_contest_id = image_contest_id and status=0
        """
        return_var = ImageContestImage.objects.values('user__id', 'image__image').filter(image_contest__contest__contest_type__code=contest_type, image_contest__status=ICA_CONTEST_TYPE_ACTIVE)
	return_var = return_var.order_by('-creation_date')

        # limits filter
        if filters_list.get("start_limit") and filters_list.get("show_limit"):
            return_var = return_var[filters_list["start_limit"]:filters_list["show_limit"]]

	# performing query
        return_var = list(return_var)

        return return_var

    # TODO
    def show_closed_contest_image(self, current_contest):
        """
        ex. -> current_contest = woman_contest
        select images where ImageContest.contest = current_contest and status=1
        """
        return True

class ImageContestVote(models.Model):
    image_contest_vote_id = models.AutoField(primary_key=True)
    image_contest_image = models.ForeignKey(ImageContestImage) # related image contest image
    ip_address = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True) # vote date

    class Meta:
        app_label = 'image_contest_app'

    def __unicode__(self):
        return str(self.image_contest_vote_id)

    def __create_votation(self, image_contest_image, ip_address):
        """Function to create a new votation"""
        return_var = False

        # create new votation
        ImageContestVote_obj = ImageContestVote(
            image_contest_image = image_contest_image,
            ip_address = ip_address,
        )

        # save votation
        ImageContestVote_obj.save()
        return_var = ImageContestVote_obj
        logger.debug("new votation created")

        return return_var

    def perform_votation(self, image_contest_image_id, ip_address, request):
        """Function to perform a votation (add image like after validity check)"""

        ImageContestImage_obj = ImageContestImage()
        ImageContestVote_obj = ImageContestVote()

        # check if image exists
        try:
            valid_image_contest_image_obj = ImageContestImage_obj.get_image_contest_image_obj(image_contest_image_id=image_contest_image_id)
        except ImageContestImage.DoesNotExist:
            # image does not exist
            raise

        try:
            ImageContestVote_obj.image_can_be_voted(image_contest_image_obj=valid_image_contest_image_obj, ip_address=ip_address, request=request)
        except ImageContestClosedError:
            # contest closed, qui si entra se sto per dare il mi piace all'utente
	    # ma qualcuno lo ha fatto prima di me, quindi sto tentando di dare un 
	    # voto in più oltre al limite massimo
            raise
        except ImageAlreadyVotedError:
            # user cannot add like to image
            raise

        # create votation
        logger.debug("creating new votation...")
        ImageContestVote_obj.__create_votation(image_contest_image=valid_image_contest_image_obj, ip_address=ip_address)

        # add like (+1) to image
        ImageContestImage_obj.add_image_like(image_contest_image_id=image_contest_image_id)

        # check if like limit is reached, then perform action "trigger_like_limit_reach"
        if ImageContestImage_obj.check_like_limit(image_contest_image_like=valid_image_contest_image_obj.like + 1):
            ImageContestImage_obj.trigger_like_limit_reach(image_contest_image_id=image_contest_image_id)

        return True

    def image_can_be_voted(self, image_contest_image_obj, ip_address, request):
        """Function to check if an image can be voted"""
	# check if contest is open
	if image_contest_image_obj.image_contest.status != ICA_CONTEST_TYPE_ACTIVE:
	    raise ImageContestClosedError

        # check if exists cookie
        if request.COOKIES.get(ICA_VATE_COOKIE_NAME + str(image_contest_image_obj.image_contest_image_id)):
            raise ImageAlreadyVotedError

	# check if exists vote inside database
	try:
	    ImageContestVote.objects.get(image_contest_image__image_contest_image_id=image_contest_image_obj.image_contest_image_id, ip_address=ip_address)
	except ImageContestVote.DoesNotExist:
	    # user can vote this catwalker
	    pass
	else:
	    # image already voted
	    raise ImageAlreadyVotedError

        return True

class ImageContestHallOfFame(models.Model):
    image_contest_hall_of_fame_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # related user
    image_contest = models.ForeignKey(ImageContest) # related image contest
    first_name = models.CharField(max_length=50, null=True) # winner user name
    last_name = models.CharField(max_length=50, null=True) # winner user last name
    image_url = models.ImageField(max_length=500, null=True) # winner user image path
    thumbnail_image_url = models.ImageField(max_length=500, null=True) # winner user thumbnail image path

    class Meta:
        app_label = 'image_contest_app'

    def __unicode__(self):
        return str(self.image_contest_hall_of_fame_id)

    # TODO
    def add_contest_hall_of_fame(self, data):
        # add image_contest_hall_of_fame element
        return True

# Create your models here.
"""
image_contest
image_contest_images
image_contest_hall_of_fame

in image_contest ho i possibili contest di immagini, possono essercene più
contemporaneamente e di tipologie differenti, a loro volta devono essere
legati al concorso principale uomo o donna. Quando l' image_contest viene
chiuso hanno una data di vita settata, oltre la quale, tutte le immagini e i
dati del contest vengono raggruppati in image_contest_hall_of_fame e le foto
eliminate

image_contest_images contiene le immagini per un dato contest, oltre alle
immagini deve contenere l'utente, i mi piace per l'immagine

image_contest_hall_of_fame contiene la foto vincente alla scadenza dell'image_contest
con altre informazioni


image_contest
(id)
contest = models.ForeignKey('Contest')
type es. monthly_beauty_and_pics (non possono esserci due image_contest con lo stesso type attivi simultaneamente nello stesso contest)
status (0 attivo per la votazione, 1 chiuso, 2 terminato, non considerarlo più)
title
creation_date
expiring

image_contest_images
(id)
image = models.OneToOneField(cropUploadedImages, primary_key=True)
user = models.ForeignKey(User)
image_contest = models.ForeignKey(image_contest)
likes

image_contest_hall_of_fame
(id)
image = models.OneToOneField(cropUploadedImages, primary_key=True)
user = models.ForeignKey(User)
image_contest = models.ForeignKey(image_contest)
date
"""
