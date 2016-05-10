# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import F
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import logging
from beauty_and_pics.consts import project_constants
from beauty_and_pics.common_utils import CommonUtils
from contest_app.models.contest_types import Contest_Type
from upload_image_box.models import cropUploadedImages 
from notify_system_app.models import Notify
from .settings import *
from .exceptions import *

# Get an instance of a logger
logger = logging.getLogger(__name__)

class PhotoContest(models.Model):
    """
    Elenco dei concorsi a tema disponibili (selfie più bello, vestito rosso,
    che eleganza, black and white, ...)
    """
    photo_contest_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200)
    contest_type = models.ForeignKey(Contest_Type) # "woman_contest" or "man_contest"
    like_limit = models.IntegerField() # image max like
    order = models.IntegerField() # element order

    class Meta:
        app_label = 'django_photo_contest'
        unique_together = ('code', 'contest_type')

    def __unicode__(self):
        return str(self.photo_contest_id) + " " + str(self.contest_type.code) + " " + str(self.code)

    def get_codes_by_contest_type(self, contest_type_code):
        return_var = None
        if contest_type_code:
            return_var = list(PhotoContest.objects.values_list("code", flat=True).filter(contest_type__code=contest_type_code))

        return return_var

    def get_photocontest_list_by_contest_type(self, contest_type_code):
        return_var = None
        if contest_type_code:
            return_var = list(PhotoContest.objects.filter(contest_type__code=contest_type_code).order_by('order'))

        return return_var

    def get_photocontest_fullinfo_list(self, contest_type_code):
        """Function to retrieve photo contest with all related info"""
        return_var = []
        photocontest_list = self.get_photocontest_list_by_contest_type(contest_type_code=contest_type_code)
        if photocontest_list:
            for photocontest in photocontest_list:
                photocontest_info = DPC_PHOTO_CONTEST_INFO.get(photocontest.code)
                photocontest_info_dict = {}
                photocontest_info_dict["code"] = photocontest.code
                photocontest_info_dict["like_limit"] = photocontest.like_limit
                photocontest_info_dict["name"] = photocontest_info.get("name")
                photocontest_info_dict["description"] = photocontest_info.get("description")
                photocontest_info_dict["rules"] = photocontest_info.get("rules")
                return_var.append(photocontest_info_dict)

        return return_var

    def get_photocontest_fullinfo(self, code, contest_type_code):
        """Function to retrieve photo contest with all related info"""
        return_var = {}
        try:
            photocontest_obj = self.get_by_code_contest_type(code=code, contest_type_code=contest_type_code)
        except PhotoContest.DoesNotExist:
            raise

        photocontest_info = DPC_PHOTO_CONTEST_INFO.get(photocontest_obj.code)
        return_var["code"] = photocontest_obj.code
        return_var["like_limit"] = photocontest_obj.like_limit
        return_var["name"] = photocontest_info.get("name")
        return_var["description"] = photocontest_info.get("description")
        return_var["rules"] = photocontest_info.get("rules")

        return return_var

    def _create_defaults(self):
        """Function to create defaults photo contests"""
        woman_photo_contest_list = self.get_codes_by_contest_type(contest_type_code=project_constants.WOMAN_CONTEST)
        man_photo_contest_list = self.get_codes_by_contest_type(contest_type_code=project_constants.MAN_CONTEST)

        logger.info("elenco codici in db: " + str(woman_photo_contest_list))
        for photocontest_code in DPC_PHOTO_CONTEST_LIST:
            if not photocontest_code in woman_photo_contest_list:
                # inserisco i contest a tema per il concorso femminile
                self.create_photo_contest(code=photocontest_code, contest_type_code=project_constants.WOMAN_CONTEST)

            if not photocontest_code in man_photo_contest_list:
                # inserisco i contest a tema per il concorso maschile
                self.create_photo_contest(code=photocontest_code, contest_type_code=project_constants.MAN_CONTEST)

        return True

    def create_photo_contest(self, code, contest_type_code):
        """Function to create a photo contest starting from photo contest code"""
        return_var = False
        contest_type_obj = Contest_Type()
        photo_contest_obj = PhotoContest()

        if code and contest_type_code:
            try:
                self.exists_code_configuration(code=code)
            except PhotocontestMissingConfiguration:
                logger.error("Il codice specificato non è presente nel file di configurazione")
                raise
            photo_contest_obj.code = code
            # salvo se è per il concorso femminile o quello maschile
            photo_contest_obj.contest_type = contest_type_obj.get_contest_type_by_code(code=contest_type_code)
            # limite di like del contest
            photo_contest_info = DPC_PHOTO_CONTEST_INFO.get(code)
            photo_contest_obj.like_limit = photo_contest_info.get("like_limit")
            photo_contest_obj.order = photo_contest_info.get("order")
            photo_contest_obj.save()
            return_var = True

        return return_var

    def exists_code_configuration(self, code):
        """Function to check if exists code configuration"""
        if not DPC_PHOTO_CONTEST_INFO.get(code):
            raise PhotocontestMissingConfiguration

        return True

    def get_by_code_contest_type(self, code, contest_type_code):
        """Function to retrieve a photocontest obj by code and contest type"""
        return_var = None
        try:
            return_var = PhotoContest.objects.get(code=code, contest_type__code=contest_type_code)
        except PhotoContest.DoesNotExist:
            raise

        return return_var

    def get_user_partecipation_photocontest(self, user_id, available_photocontest_list):
        """Function to list all photocontest in which the user play"""
        return_var = {}

        # list of all photocontest about user_id
        user_photocontest_codes_list = PhotoContestPictures.objects.values_list('photo_contest__code', flat=True).filter(user__id=user_id)

        if available_photocontest_list:
            for photocontest in available_photocontest_list:
                # controllo se l'utente sta partecipando al photocontest
                # logger.debug("codice: " + str(photocontest.get("code")) + " | lista codici presenti: " + str(user_photocontest_codes_list))
                if photocontest.get("code") in user_photocontest_codes_list:
                    # si, l'utente sta partecipando al photocontest
                    return_var[photocontest.get("code")] = True

        return return_var

class PhotoContestPictures(models.Model):
    photo_contest_pictures_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User) # related user
    photo_contest = models.ForeignKey(PhotoContest) # related photo contest
    image = models.ForeignKey(cropUploadedImages) # user image path
    like = models.IntegerField(default=0) # photo's like
    visits = models.IntegerField(default=0) # photo's visits
    insert_date = models.DateTimeField(auto_now_add=True) # photo insert date

    class Meta:
        app_label = 'django_photo_contest'
        unique_together = ('user', 'photo_contest')

    def __unicode__(self):
        return str(self.photo_contest_pictures_id) + " " + str(self.user.id) + " " + str(self.photo_contest.code)

    def exists_user_photocontest_picture(self, user_id, photocontest_code):
        """Function to check if exists user photocontest picture"""
        return PhotoContestPictures.objects.filter(user__id=user_id, photo_contest__code=photocontest_code).exists()

    def winner_image_match_photocontest_picture(self, winner_image_id, user_id, photocontest_code):
        """Function to check if exists user photocontest picture"""
        return PhotoContestPictures.objects.filter(image__id=winner_image_id, user__id=user_id, photo_contest__code=photocontest_code).exists()

    def get_user_photocontest_picture(self, user_id, photocontest_code):
        """Function to retrieve an user photocontest pictures instance"""
        try:
            return_var = PhotoContestPictures.objects.get(user__id=user_id, photo_contest__code=photocontest_code)
        except PhotoContestPictures.DoesNotExist:
            raise

        return return_var

    def add_photocontest_image_like(self, user_id, photocontest_code):
        """Function to add a photocontest image like"""

        try:
            # try to retrieve photocontest image
            photo_contest_picture_obj = self.get_user_photocontest_picture(user_id=user_id, photocontest_code=photocontest_code)
        except PhotoContestPictures.DoesNotExist:
            raise

        # add image like
        photo_contest_picture_obj.like = photo_contest_picture_obj.like + 1
        photo_contest_picture_obj.save()

        return True

    def add_photocontest_image_visit(self, photo_contest_pictures_id):
        """Function to add a photocontest image visit"""
        PhotoContestPictures.objects.filter(photo_contest_pictures_id=photo_contest_pictures_id).update(visits=F('visits') + 1)

        return True

    def calculate_remaining_like(self, photocontest_likes, photocontest_image_likes):
        """Function to calculate remaining like"""
        return int(photocontest_likes) - int(photocontest_image_likes)

    def calculate_like_perc(self, photocontest_likes, photocontest_image_likes):
        """Function to calculate remaining like"""
        return_var = 0

        if photocontest_image_likes:
            return_var = 100 / (int(photocontest_likes) / (int(photocontest_image_likes) * 1.0))

        return return_var

    def insert_photo_into_contest(self, user_id, photo_contest_id, image_id):
        """Function to insert a photo into a photocontest"""
        photo_contest_pictures_obj = PhotoContestPictures()
        photo_contest_pictures_obj.user_id = user_id
        photo_contest_pictures_obj.photo_contest_id = photo_contest_id
        photo_contest_pictures_obj.image_id = image_id
        photo_contest_pictures_obj.save()

        return True

    def get_photocontest_images(self, photo_contest_code, contest_type_code, filters_list=None):
        """
        Function to build a list of photocontest images
        i.e. -> current_contest = woman_contest
        select images where image_contest.contest.type = contest_type and status=0
        """
        return_var = PhotoContestPictures.objects.values('user__id', 'image__thumbnail_image__image').filter(photo_contest__code=photo_contest_code, photo_contest__contest_type__code=contest_type_code)
	return_var = return_var.order_by('-insert_date')

        # apply limits
        if filters_list.get("start_limit") and filters_list.get("show_limit"):
            return_var = return_var[filters_list["start_limit"]:filters_list["show_limit"]]

	# perf query
        return_var = list(return_var)

        return return_var

    def photocontest_images_exist(self, photo_contest_code, contest_type_code):
        """Function to check if exist pics into photocontest"""
        return_var = False

        if PhotoContestPictures.objects.filter(photo_contest__code=photo_contest_code, photo_contest__contest_type__code=contest_type_code).exists():
            return_var = True

        return return_var

    # TODO: testare eliminazione immagine
    def delete_user_photocontest_image(self, user_id, photocontest_code):
        """Function to delete a user photocontest image"""
        try:
            user_photocontest_picture_obj = self.get_user_photocontest_picture(user_id=user_id, photocontest_code=photocontest_code)
        except PhotoContestPictures.DoesNotExist:
            raise

        user_photocontest_picture_obj.delete()

        return True

    def clear_image_like(self, photocontest_code, contest_type_code):
        """Function to clear image likes"""
        PhotoContestPictures.objects.filter(photo_contest__code=photocontest_code, photo_contest__contest_type__code=contest_type_code).update(like=0)

        return True

    def is_photocontest_winner(self, user_id, photocontest_code, contest_type_code):
        """Function to check if a photocontest image is winning"""
        photo_contest_obj = PhotoContest()
        return_var = False

        try:
            # prelevo le informazioni sul photocontest corrente
            user_photocontest_obj = photo_contest_obj.get_photocontest_fullinfo(code=photocontest_code, contest_type_code=contest_type_code)
        except PhotoContest.DoesNotExist:
            # ERROR: photocontest doesn't exist
            logger.error("is_photocontest_winner, il photocontest non è stato trovato: photocontest_code=" + str(photocontest_code) + " contest_type_code=" + str(contest_type_code))
            pass
        else:
            try:
                # retrieve photocontest image
                user_photocontest_picture_obj = self.get_user_photocontest_picture(user_id=user_id, photocontest_code=photocontest_code)
            except PhotoContestPictures.DoesNotExist:
                # ERROR: photocontest image doesn't exist
                logger.error("is_photocontest_winner, immagine non trovata: user_id=" + str(user_id) + " photocontest_code=" + str(photocontest_code))
                pass
            else:
                if user_photocontest_picture_obj.like >= user_photocontest_obj.get("like_limit"):
                    ### this is the photocontest winner image ###
                    return_var = True

        return return_var

class PhotoContestVote(models.Model):
    """
    Per sapere se un utente può essere votato o no
    """
    photo_contest_vote_id = models.AutoField(primary_key=True)
    photo_contest_pictures = models.ForeignKey(PhotoContestPictures) # related photo contest pictures
    user = models.ForeignKey(User)
    ip_address = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'django_photo_contest'
        unique_together = ('photo_contest_pictures', 'user')

    def __unicode__(self):
        return str(self.photo_contest_vote_id)

    def check_if_user_can_add_like(self, user_id, photo_contest_pictures_id):
        """
        Function to check if a user can add like:
         - 1) controllo data ultima votazione
        """
        return_var = False

        try:
            photocontest_vote_obj = PhotoContestVote.objects.get(user__id=user_id, photo_contest_pictures__photo_contest_pictures_id=photo_contest_pictures_id)
            # 2) controllo data ultimo like
            # like già dato se vote date is < DPC_SECONDS_BETWEEN_VOTATION
            datediff = datetime.now() - photocontest_vote_obj.date
            logger.debug("datetime.now: " + str(datetime.now()))
            logger.debug("like date: " + str(photocontest_vote_obj.date))
            logger.debug("seconds: " + str(datediff.total_seconds()))
            if datediff.total_seconds() >= DPC_SECONDS_BETWEEN_VOTATION:
                # user can revote this catwalker, remove user row from db table
                photocontest_vote_obj.delete()
                return_var = True
        except PhotoContestVote.DoesNotExist:
            # l'utente non ha mai votato, votazione abilitata
            return_var = True

        return return_var

    # TODO
    def get_next_votation_date(self, user_id, photo_contest_pictures_id):
        """Function to retrieve next votation date"""
        return_var = False

        try:
            photocontest_vote_obj = PhotoContestVote.objects.get(user__id=user_id, photo_contest_pictures__photo_contest_pictures_id=photo_contest_pictures_id)
            return_var = photocontest_vote_obj.date + timedelta(seconds=DPC_SECONDS_BETWEEN_VOTATION + 60) # NOTA: sommo 60 secondi altrimenti la funzione nel template mi farebbe vedere: mancano 0 minuti, per evitarlo ho sommato i 60
            # return_var = relativedelta(datetime.now(), photocontest_vote_obj.date)
            logger.debug("get_next_votation_date: " + str(return_var))
        except PhotoContestVote.DoesNotExist:
            # l'utente non ha mai votato, non è presente una next votation date
            pass

        return return_var

    def create_votation(self, user_id, photo_contest_pictures_id, request):
	"""Function to add a new votation"""
	photocontest_vote_obj = PhotoContestVote()
        common_utils_obj = CommonUtils()

	# il photocontest esiste, procedo con l'inserimento della votazione
	photocontest_vote_obj.photo_contest_pictures_id = photo_contest_pictures_id
	photocontest_vote_obj.user_id = user_id
	photocontest_vote_obj.ip_address = common_utils_obj.get_ip_address(request=request)
 	photocontest_vote_obj.save()

	return True

    def delete_photocontest_vote(self, photocontest_code, contest_type_code):
        """Function to delete all votes about a photocontest"""
        PhotoContestVote.objects.filter(photo_contest_pictures__photo_contest__code=photocontest_code, photo_contest_pictures__photo_contest__contest_type__code=contest_type_code).delete()

        return True

class PhotoContestWinner(models.Model):
    """
    I vincitori dei vari photocontest verranno salvati qui, ogni utente
    quindi potrebbe avere più righe per lo stesso photo contest
    """
    photo_contest_winner_id = models.AutoField(primary_key=True)
    photo_contest = models.ForeignKey(PhotoContest) # related photo contest
    user = models.ForeignKey(User) # related user
    image = models.ForeignKey(cropUploadedImages) # user image path
    creation_date = models.DateTimeField(auto_now_add=True) # photo winning date

    class Meta:
        app_label = 'django_photo_contest'

    def __unicode__(self):
        return str(self.photo_contest_winner_id) + " " + str(self.user.id) + " " + str(self.photo_contest.code)

    def manage_photocontest_winner(self, user_id, photocontest_code, contest_type_code):
        """Function to manage a photocontest winner"""
        photo_contest_vote_obj = PhotoContestVote()
        photo_contest_pictures_obj = PhotoContestPictures()

        try:
            # inserisco il vincitore in PhotoContestWinner
            self.add_contest_winner(user_id=user_id, photocontest_code=photocontest_code, contest_type_code=contest_type_code)
        except PhotoContestPictures.DoesNotExist:
            raise

        # XXX: per ora no
        # elimino tutti i voti per il contest_type_code e il photocontest_code
        # photo_contest_vote_obj.delete_photocontest_vote(photocontest_code=photocontest_code, contest_type_code=contest_type_code)

        # azzero tutti voti dell'immagine
        photo_contest_pictures_obj.clear_image_like(photocontest_code=photocontest_code, contest_type_code=contest_type_code)

        return True

    def add_contest_winner(self, user_id, photocontest_code, contest_type_code):
        """Function to add a new photocontest winner"""
        photocontest_pictures_obj = PhotoContestPictures()
	photo_contest_obj = PhotoContest()
        points_added = False

        try:
	    # prelevo il concorso dell'immagine vincitrice
	    user_photo_contest_obj = photo_contest_obj.get_by_code_contest_type(code=photocontest_code, contest_type_code=contest_type_code)
        except PhotoContest.DoesNotExist:
            raise

        try:
	    # prelevo l'immagine vincitrice
            user_photocontest_pictures_obj = photocontest_pictures_obj.get_user_photocontest_picture(user_id=user_id, photocontest_code=photocontest_code)
        except PhotoContestPictures.DoesNotExist:
            raise

	photo_contest_winner_obj = PhotoContestWinner()
	photo_contest_winner_obj.user_id = user_id
	photo_contest_winner_obj.photo_contest = user_photo_contest_obj
	photo_contest_winner_obj.image = user_photocontest_pictures_obj.image
	photo_contest_winner_obj.save()

        if DPC_ADD_WINNER_POINTS:
            # assegno i punti al vincitore
            points_added = self.assign_user_points(to_user_obj=user_photocontest_pictures_obj.user)

        if DPC_WRITE_WINNER_NOTIFY:
            # scrivo la notifica all'utente vincitore
            photocontest_info = DPC_PHOTO_CONTEST_INFO.get(photocontest_code) # (per prelevare il nome del photocontest)
            self.notify_to_winning_user(user_id=user_id, photocontest_name=photocontest_info.get("name"), points_added=points_added)

        return True

    # TODO
    def assign_user_points(self, to_user_obj):
	from contest_app.models.votes import Vote
        vote_obj = Vote()
        return_var = False

        # setto i punti da assegnare
        metrics_points = {
            project_constants.VOTE_METRICS_LIST["smile_metric"] : 8,
            project_constants.VOTE_METRICS_LIST["look_metric"] : 8,
            project_constants.VOTE_METRICS_LIST["global_metric"] : 8,
            project_constants.VOTE_METRICS_LIST["style_metric"] : 8,
        }

        # assegno i punti (solo se il contest è aperto)
        return_var = vote_obj.add_metrics_points(metrics_points=metrics_points, to_user_obj=to_user_obj)

        return return_var

    # TODO: testare
    def notify_to_winning_user(self, user_id, photocontest_name, points_added=False):
        """Function to write a notify to a winning user"""
        notify_obj = Notify()

        # create notify details
        if points_added:
            # il concorso è aperto ed ho aggiunto dei punti
            notify_data = {
                "title" : "La tua foto ha vinto il concorso a tema '" + str(photocontest_name) + "'.",
                "message" : "Complimenti, ottenendo il maggior numero di \"Mi piace\" hai vinto il bonus di <b>+32 punti</b> nella classifica generale e il posto in <b>evidenza</b> nel concorso a tema '" + str(photocontest_name) + "'.<br />Continua ad accumulare voti per rimanere in testa.",
            }
        else:
            # il concorso è chiuso e quindi non ho potuto aggiungere dei punti
            notify_data = {
                "title" : "La tua foto ha vinto il concorso a tema '" + str(photocontest_name) + "'.",
                "message" : "Complimenti, ottenendo il maggior numero di \"Mi piace\" hai vinto il posto in <b>evidenza</b> nel concorso a tema '" + str(photocontest_name) + "'.<br />Continua ad accumulare voti per rimanere in testa.",
            }

        # save notify about this user
        notify_obj.create_notify(data=notify_data, user_id=user_id)

        return True

    def get_last_photocontest_winner(self, photocontest_code, contest_type_code):
        """Function to retrieve last photocontest winner if exists"""
        photo_contest_pictures_obj = PhotoContestPictures()
        return_var = {}

        last_photocontest_winner_list = PhotoContestWinner.objects.filter(photo_contest__code=photocontest_code, photo_contest__contest_type__code=contest_type_code).order_by('-creation_date')[:1]

        if last_photocontest_winner_list:
            last_photocontest_winner = last_photocontest_winner_list[0]
            return_var["image_url"] = last_photocontest_winner.image.image.url

            # controllo che l'immagine esista ancora nel photocontest
            if photo_contest_pictures_obj.winner_image_match_photocontest_picture(winner_image_id=last_photocontest_winner.image.id, user_id=last_photocontest_winner.user.id, photocontest_code=photocontest_code):
                # se esiste il link punta alla foto
                return_var["vote_image_url"] = "/concorsi-a-tema/" + str(photocontest_code) + "/" + str(last_photocontest_winner.user.id) + "/"
            else:
                # se non esiste il link punta al profilo utente
                return_var["vote_image_url"] = "/passerella/dettaglio-utente/" + str(last_photocontest_winner.user.id) + "/"

        return return_var

    # TODO
    def check_if_image_is_winning(self, user_id, photocontest_code, contest_type_code):
	"""Function to check if current image is a winning image"""
        photo_contest_pictures_obj = PhotoContestPictures()
        return_var = False
	last_photocontest_winning_image = False

	# prelevo l'ultima immagine vincitrice
        last_photocontest_winning_list = PhotoContestWinner.objects.filter(photo_contest__code=photocontest_code, photo_contest__contest_type__code=contest_type_code).order_by('-creation_date')[:1]
        if last_photocontest_winning_list:
            last_photocontest_winning_image = last_photocontest_winning_list[0]

	# prelevo l'immagine dell'attuale photocontest
	try:
	    user_photo_contest_pictures_obj = photo_contest_pictures_obj.get_user_photocontest_picture(user_id=user_id, photocontest_code=photocontest_code)
        except PhotoContestPictures.DoesNotExist:
            pass

	if last_photocontest_winning_image and user_photo_contest_pictures_obj:
	    if last_photocontest_winning_image.image_id == user_photo_contest_pictures_obj.image_id:
		return_var = True

        return return_var

"""
Per partecipare ai sottoconcorsi occorre:
    - aver verificato il proprio account
    - aver caricato la foto profilo
    - aver caricato almeno 3 immagini del book

Ci sarà una pagina nel profilo privato che mostrerà l'elenco dei concorsi
fotografici disponibili (con la solita visualizzazione a griglia del pannello
di controllo), per ognuno mostro se l'utente è già un partecipante o no.
Cliccando su un concorso a tema si aprirà un popup con
immagine, descrizione del concorso e relativi vincoli, con due pulsanti, <partecipa> <annulla>

Cliccando su partecipa si andrà nella pagina già creata per l'app
image_contest, dove chiederò all'utente di selezionare una foto dal proprio
book, a selezione e conferma effettuata, andrò in un ulteriore pagina dove
mostrerò le statistiche dell'immagine per quel dato concorso: click ricevuto,
numero di visite, click mancanti, sarà inoltre possibile rimuovere l'immagine
dal sottoconcorso.

L'azione soprà creerà una pagina pubblica dalla quale sarà possibile assegnare
il "mi piace" alla foto, la prima foto che raggiungerà i "Mi piace" prima
delle altre sarà decretata vincitrice ed inserita all'interno di
PhotoContestWinner, il concorso a questo punto verrà svuotato da tutte le foto
partecipanti.

L'ultimo vincitore del concorso sarà messo in bella mostra da qualche parte.

[Addizionalmente fare una tabella con i trofei, alla vincita di un concorso
assegnare ad un partecipante un trofeo e mostrarlo nella pagina profilo.]
"""
