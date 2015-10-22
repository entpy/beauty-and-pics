# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from contest_app.models.contest_types import Contest
from .settings import *
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
logger_app_prefix = "image_contest_app"

class ImageContest(models.Model):
    id_image_contest = models.AutoField(primary_key=True)
    contest = models.ForeignKey(Contest) # woman contest or man contest
    title = models.CharField(max_length=200) # contest title, ex. "Best pics contest!"
    type = models.CharField(max_length=50) # contest type, ex. best_photo
    status = models.IntegerField(default=0) # (0 attivo per la votazione, 1 chiuso, 2 terminato => non considerarlo più)
    creation_date = models.DateTimeField(auto_now_add=True) # contest creation date
    expiring = models.DateTimeField(null=True) # contest expiring
    like_limit = models.IntegerField(null=True) # image max like

    class Meta:
        app_label = 'image_contest_app'

    def __unicode__(self):
        return str(self.id_image_contest) + " " + str(self.type) + " " + str(self.creation_date)

    def manage_image_contest(self):
        """
        Chiudo i contest che sono da chiudere
        Creo i contest che sono da aprire
        """
        return True

    def __close_expired_contests(self):
        # chiudo i contest scaduti e salvo tutto in ImageContestHallOfFame
        return True

    def __create_contests(self):
        # creo i nuovi image contest, uno per il man contest e l'altro per il woman contest
        return True

class ImageContestImage(models.Model):
    id_image_contest_image = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # related user
    image_contest = models.ForeignKey(ImageContest) # related image contest
    image = models.ImageField(max_length=500, null=True) # user image path
    thumbnail_image = models.ImageField(max_length=500, null=True) # user thumbnail image path
    like = models.IntegerField(default=0) # image's like

    class Meta:
        app_label = 'image_contest_app'

    def __unicode__(self):
        return str(self.id_image_contest_image) + " " + str(self.image.image.url)

    def add_contest_image(self, data):
        # add image_contest_image element
        return True

    def remove_contest_image(self, id_image_contest_image):
        # remove image_contest_image element
        return True

    def add_image_like(self, id_image_contest_image, like=1)
        # add a like (+1) to image
        return True

    def trigger_like_limit_reach(self, id_image_contest_image):
        # action performed when like limit is reached
        return True

    def check_like_limit(self, id_image_contest_image):
        # check if like limit is reached, then perfoming "trigger_like_limit_reach" function
        return True

    def show_contest_all_images(self, current_contest):
        """
        ex. -> current_contest = woman_contest
        select images where ImageContest.contest = current_contest and status=0
        """
        return True

    def show_closed_contest_image(self, current_contest):
        """
        ex. -> current_contest = woman_contest
        select images where ImageContest.contest = current_contest and status=1
        """
        return True

class ImageContestHallOfFame(models.Model):
    id_image_contest_hall_of_fame = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # related user
    image_contest = models.ForeignKey(ImageContest) # related image contest
    first_name = models.CharField(max_length=50, null=True) # winner user name
    last_name = models.CharField(max_length=50, null=True) # winner user last name
    image = models.ImageField(max_length=500, null=True) # winner user image path
    thumbnail_image = models.ImageField(max_length=500, null=True) # winner user thumbnail image path

    class Meta:
        app_label = 'image_contest_app'

    def __unicode__(self):
        return str(self.id_image_contest_hall_of_fame)

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
