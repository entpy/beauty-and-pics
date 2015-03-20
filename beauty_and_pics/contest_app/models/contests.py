# -*- coding: utf-8 -*-

from django.db import models
from datetime import timedelta
from django.utils import timezone
from contest_app.models.contest_types import Contest_Type
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Contest(models.Model):
    id_contest = models.AutoField(primary_key=True)
    id_contest_type = models.ForeignKey('Contest_Type')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)

    class Meta:
        app_label = 'contest_app'

    def __unicode__(self):
        return str(self.id_contest) + " " + str(self.id_contest_type.code)

    """
            * id_contest (PK)
            * id_contest_type
            * start_date
            * end_date
            * status (0 in attesa di apertura, 1 attivo, 2 chiuso)
    """

    def __create_contests(self):
        """Function to create contests
        Funzione per creare i concorsi()

        Itero sui tipi di concorso con tipo_status=1 (solo quelli attivi, per ora "uomo" e "donna")
            Se per ogni tipo non esiste il concorso attivo (con concorso.status=1)
                - creo il concorso, ponendo come start_date "+ 1 mese" a partire dalla data attuale
                e mettendo lo status a 0 (default)
                - notifico tutti gli utenti appartenenti al concorso che tra un mese
                  aprirà il concorso

        """
        for contest_type in Contest_Type.objects.all():
            if not Contest.objects.filter(id_contest_type=contest_type.id_contest_type, status=1).count():
                # no active contest, must be create a new one
                Contest_obj = Contest()
                Contest_obj.id_contest_type = contest_type
                # Contest_obj.start_date = timezone.now()+timedelta(days=35)
                # XXX: debug, use this --^
                Contest_obj.start_date = timezone.now()-timedelta(days=2)
                Contest_obj.save()
                # send email
                logger.info("contest creato: " + str(Contest_obj))

        return True

    def __close_contests(self):
        """Function to close contests
        Funzione per chiudere i concorsi()

        itero su tutti i concorsi attivi (status=1)
            se la data corrente è >= della scadenza del concorso
                - chiudo il concorso (settando lo status=2  |1 -> 2|)
                - notifico tutti gli utenti (TUTTI!) che il concorso è stato chiuso

        """
        for contest in Contest.objects.filter(status=1):
            if timezone.now() >= contest.end_date:
                # send email
                logger.info("contest chiuso:" + str(contest))
                pass
        Contest.objects.filter(status=1, end_date__lte=timezone.now()).update(status=2)

        return True

    def __activate_contests(self):
        """Function to activate contests
        Funzione per attivare i concorsi()

        itero su tutti i concorsi in attesa di apertura (status=0)
            se la data corrente è >= della "start_date"del concorso
                - apro il concorso (settando lo status=1  |0 -> 1|)
                ponendo come end_date "+ 10 mesi" a partire dalla data attuale
                - notifico tutti gli utenti (TUTTI!) che il concorso è stato aperto
        """
        for contest in Contest.objects.filter(status=0):
            if timezone.now() >= contest.start_date:
                # send email
                logger.info("contest attivato:" + str(contest))
                pass
        Contest.objects.filter(status=0, start_date__lte=timezone.now()).update(status=1, end_date=(timezone.now()+timedelta(days=330)))

        return True

    def contest_manager(self):
        """Function to manage contests"""
        logger.info("gestore dei contest")
        self.__close_contests()
        self.__create_contests()
        self.__activate_contests()

        return True

    """
    Le funzioni devono essere eseguite in quest'ordine:
    __close_contests()
    __create_contests()
    __activate_contests()
    """

    def get_contests_expiring(self):
        """Function to calculate expiration about all active contests"""
        # update contests
        return_var = {}
        self.contest_manager()
        for contest in Contest.objects.filter(status=1):
            # return_var[contest.id_contest_type.code] = contest.end_date - timezone.now()
            contest_expiring = contest.end_date - timezone.now()
            return_var[contest.id_contest_type.code]["days"] = contest_expiring.days
            return_var[contest.id_contest_type.code]["hours"] = contest_expiring.seconds // 3600 # 3600 = 60 min * 60 sec (sec in 1 hour)
            return_var[contest.id_contest_type.code]["minutes"] = contest_expiring.seconds // 60 % 60
            return_var[contest.id_contest_type.code]["seconds"] = contest_expiring.seconds % 60
            return_var[contest.id_contest_type.code] = {""}contest_expiring.seconds % 60

        """
        days = return_var["woman_contest"].days
        hours = return_var["woman_contest"].seconds // 3600 # 3600 = 60 min * 60 sec (sec in 1 hour)
        minutes = return_var["woman_contest"].seconds // 60 % 60
        seconds = return_var["woman_contest"].seconds % 60
        """
        logger.info("man_contest scadenza:" + str(return_var["man_contest"]))
        logger.info("woman_contest ore scadenza:" + str(return_var["woman_contest"]))

        return return_var
