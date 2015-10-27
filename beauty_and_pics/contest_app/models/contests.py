# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from contest_app.models.contest_types import Contest_Type
from contest_app.models.metrics import Metric
from beauty_and_pics.consts import project_constants
import logging, time

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Contest(models.Model):
    id_contest = models.AutoField(primary_key=True)
    contest_type = models.ForeignKey('Contest_Type')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=25)

    class Meta:
        app_label = 'contest_app'

    def __unicode__(self):
        return str(self.id_contest) + " " + str(self.contest_type.code)

    """
            * id_contest (PK)
            * contest_type
            * start_date
            * end_date
            * status (0 in attesa di apertura, 1 attivo, 2 chiuso)
    """

    def __create_contests(self):
        """Function to create contests
        Funzione per creare i concorsi()

        Itero sui tipi di concorso con tipo_status=1 (solo quelli attivi, per ora "uomo" e "donna")
            Se per ogni tipo non esiste il concorso attivo o in fase di
            apertura (con concorso.status!=0 o concorso.status=1)
                - creo il concorso, ponendo come start_date "+ 1 mese" a partire dalla data attuale
                  e mettendo lo status a 0 (default)
                - notifico tutti gli utenti appartenenti al concorso che tra un mese
                  aprirà il concorso
        """
        for contest_type in Contest_Type.objects.all():
            if not Contest.objects.filter(Q(contest_type=contest_type.id_contest_type), Q(status=project_constants.CONTEST_OPENING) | Q(status=project_constants.CONTEST_ACTIVE)).count():
                # no active or opening contests, must be create a new one
                Contest_obj = Contest(
                    contest_type = contest_type,
                    start_date = timezone.now() + timedelta(days=project_constants.CONTEST_OPENING_DAYS),
                    status = project_constants.CONTEST_OPENING,
                )
                Contest_obj.save()
                # send an email
                logger.info("contest creato: " + str(Contest_obj))

        return True

    def __close_contests(self):
        from contest_app.models.hall_of_fame import HallOfFame
        from account_app.models.accounts import Account
        """Function to close contests
        Funzione per chiudere i concorsi()

        itero su tutti i concorsi attivi (status=1)
            se la data corrente è >= della scadenza del concorso
                - chiudo il concorso (settando lo status=2  |1 -> 2|)
                - notifico tutti gli utenti (TUTTI!) che il concorso è stato chiuso

        """
        send_email = False
        contest_list = Contest.objects.filter(status=project_constants.CONTEST_ACTIVE)
        for contest in contest_list:
            if timezone.now() >= contest.end_date:
                logger.info("contest chiuso:" + str(contest))
                # save best users inside hall of fame
                hall_of_fame_obj = HallOfFame()
                hall_of_fame_obj.save_active_contest_hall_of_fame(contest_type=contest.contest_type.code)
                send_email = True
                pass
        Contest.objects.filter(status=project_constants.CONTEST_ACTIVE, end_date__lte=timezone.now()).update(status=project_constants.CONTEST_CLOSED)

        # send emails
        if send_email and contest_list:
            for contest in contest_list:
                if timezone.now() >= contest.end_date:
                    # send close contest emails
                    account_obj = Account()
                    account_obj.send_contest_closing_emails(contest_type=contest.contest_type.code)

        return True

    def __activate_contests(self):
        from account_app.models.accounts import Account
        """Function to activate contests
        Funzione per attivare i concorsi()

        itero su tutti i concorsi in attesa di apertura (status=0)
            se la data corrente è >= della "start_date"del concorso
                - apro il concorso (settando lo status=1  |0 -> 1|)
                ponendo come end_date "+ 10 mesi" a partire dalla data attuale
                - notifico tutti gli utenti (TUTTI!) che il concorso è stato aperto
        """
        send_email = False
        contest_list = Contest.objects.filter(status=project_constants.CONTEST_OPENING)
        for contest in contest_list:
            if timezone.now() >= contest.start_date:
                logger.info("contest attivato:" + str(contest))
                send_email = True
                pass
        Contest.objects.filter(status=project_constants.CONTEST_OPENING, start_date__lte=timezone.now()).update(status=project_constants.CONTEST_ACTIVE, end_date=(timezone.now()+timedelta(days=project_constants.CONTEST_EXPIRING_DAYS)))

        # send emails
        if send_email and contest_list:
            for contest in contest_list:
                if timezone.now() >= contest.start_date:
                    # send open contest emails
                    account_obj = Account()
                    account_obj.send_contest_opening_emails(contest_type=contest.contest_type.code)

        return True

    def __create_default_types(self):
        """creating contest type firstly, if not exists"""
        Contest_Type_obj = Contest_Type()
        Contest_Type_obj.create_default()

        return True

    def contest_manager(self):
        """Function to manage contests"""
        logger.info("gestore dei contest")
        # create default metrics
        metric_obj = Metric()
        metric_obj.metrics_manager()

        # solo per debug, scriptizzarlo e inviarlo max 1 volta al mese
        # per ogni account
        # account_obj.send_report_emails(contest_type="woman-contest")

        # create contests
        self.__create_default_types()
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

    def contest_report(self):
        """Send emails for each open contests"""
        from account_app.models.accounts import Account
        account_obj = Account()
        return_var = False
        for contest in Contest.objects.filter(status=project_constants.CONTEST_ACTIVE):
            account_obj.send_report_emails(contest_type=contest.contest_type.code)
            return_var = True

        return return_var

    def format_contest_time(self, date=None):
        """Function to format the contest start/end date as dictionary"""
        return_var = None

        if date:
            return_var = {
                "days": date.days,
                "hours": date.seconds // 3600, # 3600 = 60 min * 60 sec (sec in 1 hour)
                "minutes": date.seconds // 60 % 60,
                "seconds": date.seconds % 60,
                "total_seconds": int(date.total_seconds()),
            }

        return return_var

    def get_all_active_contests(self):
        """Function to retrieve all active constests"""
        return_var = False
        return_var = Contest.objects.filter(status=project_constants.CONTEST_ACTIVE)
        return return_var

    def get_active_contests_end_time(self, update_contests=False):
        """Function to retrieve end time info about all active constests"""
        return_var = {}
        # update contests
        if update_contests:
            self.contest_manager()
        # list of all active contests
        for contest in Contest.objects.filter(status=project_constants.CONTEST_ACTIVE):
            # contest_expiring = contest.end_date - timezone.now()
            # return_var[contest.contest_type.code] = self.format_contest_time(date=contest_expiring)
            contest_expiring = contest.end_date.timetuple()
            return_var[contest.contest_type.code] = int(time.mktime(contest_expiring) * 1000)

        # debug info only
        for contest in Contest.objects.filter(status=project_constants.CONTEST_ACTIVE):
            logger.info(str(contest.contest_type.code) + " scadenza:" + str(return_var[contest.contest_type.code]))

        return return_var

    def get_opening_contests_start_time(self, update_contests=False):
        """Function to retrieve start time info about all opening constests"""
        return_var = {}
        # update contests
        if update_contests:
            self.contest_manager()
        # list of all opening contests
        for contest in Contest.objects.filter(status=project_constants.CONTEST_OPENING):
            # contest_opening = contest.start_date - timezone.now()
            # return_var[contest.contest_type.code] = self.format_contest_time(date=contest_opening)
            contest_opening = contest.start_date.timetuple()
            return_var[contest.contest_type.code] = int(time.mktime(contest_opening) * 1000)

        # debug info only
        for contest in Contest.objects.filter(status=project_constants.CONTEST_OPENING):
            logger.info(str(contest.contest_type.code) + " inizio:" + str(return_var[contest.contest_type.code]))

        return return_var

    def get_contests_type_status(self, contest_type=None):
        """Function to retrieve contest status about a contest_type"""
        return_var = None
        if contest_type:
            contest_obj = Contest()
            if Contest.objects.filter(status=project_constants.CONTEST_OPENING, contest_type__code=contest_type).count():
                return_var = project_constants.CONTEST_OPENING
            elif Contest.objects.filter(status=project_constants.CONTEST_ACTIVE, contest_type__code=contest_type).count():
                return_var = project_constants.CONTEST_ACTIVE

        return return_var

    def get_active_contests_by_type(self, contest_type):
        """Function to retrieve active contest by contest_type"""
        return_var = None
	try:
            return_var = Contest.objects.get(status=project_constants.CONTEST_ACTIVE, contest_type__code=contest_type)
	except Contest.DoesNotExist:
	    pass

        return return_var

    def get_last_active_contests_by_type(self, contest_type):
        """Function to retrieve last active contest by contest_type"""
        return_var = None
        last_contest_list = Contest.objects.filter(status=project_constants.CONTEST_ACTIVE, contest_type__code=contest_type).order_by('-id_contest')
        if last_contest_list:
            return_var = last_contest_list[0]

        return return_var

    def get_last_closed_contests_by_type(self, contest_type):
        """Function to retrieve last active contest closed by contest_type"""
        return_var = None
        last_contest_list = Contest.objects.filter(status=project_constants.CONTEST_CLOSED, contest_type__code=contest_type).order_by('-id_contest')
        if last_contest_list:
            return_var = last_contest_list[0]

        return return_var

    def get_contest_info_about_type(self, contest_type):
        """Function to retrieve contest info about contest_type"""
        return_var = {}
        if contest_type:
            contest_status = self.get_contests_type_status(contest_type=contest_type)
            if contest_status == project_constants.CONTEST_OPENING:
                # return opening contest start_time
                opening_contests = self.get_opening_contests_start_time()
                if opening_contests.get(contest_type):
                    return_var["timedelta"] = opening_contests[contest_type]
                    return_var["status"] = project_constants.CONTEST_OPENING
		    logger.debug("apertura del contest[" + str(contest_type) + "]: " + str(return_var["timedelta"]))
            elif contest_status == project_constants.CONTEST_ACTIVE:
                # return active contest end_time
                active_contests = self.get_active_contests_end_time()
                if active_contests.get(contest_type):
                    return_var["timedelta"] = active_contests[contest_type]
                    return_var["status"] = project_constants.CONTEST_ACTIVE

        return return_var

    def get_contest_type_from_user_id(self, user_id=None):
        """Function to retrieve contest_type from user id"""
        from account_app.models.accounts import Account
        return_var = False
        account_obj = Account()

        # retrieve contest_type from user id
        account_info = account_obj.custom_user_id_data(user_id=user_id)
        if account_info["contest_type"]:
            return_var = account_info["contest_type"]
        else:
            # retrieve default contest_type
            return_var = self.get_default_contest_type()

        return return_var

    def get_default_contest_type(self):
        """Function to retrieve default contest_type"""
        return project_constants.WOMAN_CONTEST

    def get_contest_type_from_session(self, request):
        """Function to retrieve contest type from session"""
        return_var = None
        if request.session.get("contest_type"):
            return_var = request.session.get("contest_type")
        else:
            return_var = self.get_default_contest_type()

        return return_var

    def contest_type_exists_check(self, contest_type=None):
        """Function to check if a contest_type name is valid"""
        return_var = False
        if contest_type == project_constants.WOMAN_CONTEST:
            return_var = True
        elif contest_type == project_constants.MAN_CONTEST:
            return_var = True

        return return_var

    def set_contest_type(self, request, contest_type=None):
        """Function to save contest_type identified into session"""
        return_var = False
        if contest_type:
            # only if contest type exists
            if self.contest_type_exists_check(contest_type=str(contest_type)):
                request.session['contest_type'] = str(contest_type)
                return_var = True

        return return_var

    def get_contest_year(self, contest=None):
        """Function to retrieve start_date year about a contest"""
        return_var = False
        if contest:
            return_var = contest.start_date.year
        return return_var
