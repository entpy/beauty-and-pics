# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from contest_app.models.contest_types import Contest_Type
from upload_image_box.models import cropUploadedImages 
from .settings import *
from .exceptions import *
from beauty_and_pics.consts import project_constants
import logging

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
            return_var = list(PhotoContest.objects.filter(contest_type__code=contest_type_code))

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

    def exists_user_photocontest(self, user_id, photocontest_code):
        """Function to check if exists user photocontest picture"""
        return PhotoContestPictures.objects.filter(user__id=user_id, photo_contest__code=photocontest_code).exists()

    def insert_photo_into_contest(self, user_id, photo_contest_id, image_id):
        """Function to insert a photo into a photocontest"""
        photo_contest_pictures_obj = PhotoContestPictures()
        photo_contest_pictures_obj.user_id = user_id
        photo_contest_pictures_obj.photo_contest_id = photo_contest_id
        photo_contest_pictures_obj.image_id = image_id
        photo_contest_pictures_obj.save()

        return True

class PhotoContestVote(models.Model):
    """
    Per sapere se un utente può essere votato o no
    """
    photo_contest_vote_id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(User, related_name='photocontest_vote_from_user')
    to_user = models.ForeignKey(User, related_name='photocontest_vote_to_user')
    ip_address = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'django_photo_contest'

    def __unicode__(self):
        return str(self.photo_contest_vote_id)

class PhotoContestWinner(models.Model):
    """
    I vincitori dei vari photo contest verranno salvati qui, ogni utente
    quindi potrebbe avere più righe per lo stesso photo contest
    """
    photo_contest_winner_id = models.AutoField(primary_key=True)
    photo_contest = models.ForeignKey(PhotoContest) # related photo contest
    user = models.ForeignKey(User) # related user
    image_url = models.ImageField(max_length=500, null=True) # winner user image path
    thumbnail_image_url = models.ImageField(max_length=500, null=True) # winner user thumbnail image path
    creation_date = models.DateTimeField(auto_now_add=True) # photo winning date

    class Meta:
        app_label = 'django_photo_contest'

    def __unicode__(self):
        return str(self.photo_contest_winner_id) + " " + str(self.user.id) + " " + str(self.photo_contest.code)

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
