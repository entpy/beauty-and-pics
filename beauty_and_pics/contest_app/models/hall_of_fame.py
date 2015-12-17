# -*- coding: utf-8 -*-

from django.db import models
from contest_app.models.contests import Contest
from django.contrib.auth.models import User
from account_app.models.images import Book
from beauty_and_pics.consts import project_constants
from website.exceptions import ContestClosedNotExistsError, ContestTypeRequiredError
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class HallOfFame(models.Model):
    id_hall_of_fame = models.AutoField(primary_key=True)
    contest = models.ForeignKey('Contest')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    ranking = models.IntegerField()
    points = models.IntegerField()
    disqualified = models.IntegerField(default=0)

    class Meta:
        app_label = 'contest_app'

    def __unicode__(self):
        return str(self.id_hall_of_fame)

    """
        * id_hall_of_fame (PK)
        * contest (FK)
        * user (FK)
        * ranking
        * points
    """

    def save_active_contest_hall_of_fame(self, contest_type):
        """Function to create hall of fame about a contest (before contest close action)"""
        from account_app.models.accounts import Account
        contest_obj = Contest()
        account_obj = Account()

        # retrieve best 100 users about current contest_type
        top_users = account_obj.get_top_100_contest_user(contest_type=contest_type)

        # retrieve active contest
        active_contest = contest_obj.get_active_contests_by_type(contest_type=contest_type)
        if top_users:
            ranking = 1
            for single_user in top_users:
                # save user inside hall of fame *.*
                hall_of_fame_obj = HallOfFame()
                hall_of_fame_obj.contest = active_contest
                hall_of_fame_obj.user = single_user["user"]
                hall_of_fame_obj.ranking = ranking
                hall_of_fame_obj.points = single_user["user_total_points"]
                hall_of_fame_obj.save()
                ranking +=1

        return True

    # TODO: testare elenco utenti per contest e anno.
    # testare anche utente vincitore
    def get_contest_top_100(self, contest_type, contest_year, user_id=False):
        """Function to retrieve top 100 users about a contest"""
        return_var = None
        Contest_obj = Contest()

	# filter contest_type
	return_var = HallOfFame.objects.values(
		'contest__start_date',
		'user__id',
		'user__first_name',
		'user__last_name',
		'ranking',
		'points',
		'disqualified',
		).filter(contest__contest_type__code=contest_type)

	# filter year
	return_var = return_var.filter(contest__start_date__year=contest_year)

        # check if retrieve only a single user
        if user_id:
            return_var = return_var.filter(user__id=user_id)

	# order by ranking
	return_var = return_var.order_by('ranking')

        return return_var

    def get_hall_of_fame_user(self, contest_type, contest_year=False, user_id=False):
	"""Function to retrieve last active contest winner"""
	return_var = None
	Book_obj = Book()

	logger.info("prelevo un utente specifico tra i top 100, contest: " + str(contest_type) + ", contest_year: " + str(contest_year) + ", user_id: " + str(user_id))

	try:
	    return_var = self.get_hall_of_fame_elements(contest_type=contest_type, contest_year=contest_year, user_id=user_id)
	except ContestTypeRequiredError:
	    raise
	except ContestClosedNotExistsError:
	    raise

	if return_var:
	    # sia che voglia avere solo il vincitore, oppure un determinato utente,
	    # prelevo solo il primo elemento della lista
	    return_var = return_var[0]

            if return_var["disqualified"]:
                # l'utente è stato squalificato per una serie di motivi, sarà
                # visibile in classifica senza punteggio e non ci sarà foto in home e passerella
                return_var = None
            else:
                # carico anche l'immagine profilo dell'utente prelevato
                logger.info("prelevo immagine profilo per user: " + str(return_var))
                return_var["profile_image"] = Book_obj.get_profile_thumbnail_image_url(user_id=return_var["user__id"])
                return_var["profile_thumbnail_image"] = Book_obj.get_profile_image_url(user_id=return_var["user__id"])

        return return_var

    def get_hall_of_fame_elements(self, contest_type, contest_year=False, user_id=False):
	"""
	    Function to retrieve an elements list of a single element about hall of fame object:
	    - se non viene passato un anno, viene utilizzato l'anno dell'ultimo contest attivo
	    - se non viene passato l'anno e non esistono contest precedentemente chiusi throwa un folle errore
	"""
	return_var = None
        Book_obj = Book()
	Contest_obj = Contest()

	if not contest_type:
	    # non è stato specificato un contest_type
	    raise ContestTypeRequiredError

	if not contest_year:
	    # tento di prelevare l'anno dell'ultimo concorso chiuso
	    try:
		contest_year = Contest_obj.get_last_closed_contests_year(contest_type=contest_type)
	    except ContestClosedNotExistsError:
		# non esiste ancora un contest chiuso per questo contest_type
		raise

        return_var = self.get_contest_top_100(contest_type=contest_type, contest_year=contest_year, user_id=user_id)

        return return_var

    def is_a_podium_user(self, hall_of_fame_user_row):
        """Function to check if a user is a podium user"""
        return_var = False

        if hall_of_fame_user_row:
            if int(hall_of_fame_user_row.get("ranking")) >= 1 and int(hall_of_fame_user_row.get("ranking")) <= 5:
                return_var = True

        return return_var

    def get_podium_page_string(self, contest_type, ranking):
        """
            Function to build podium page string, related with ranking and contest_type
            es. "Vincitrice assoluta" or "Terzo classificato"
        """
        return_var = ""

        # check contest type
        if contest_type == project_constants.WOMAN_CONTEST:
            # check podium user ranking
            if ranking == 1:
                return_var = "Vincitrice assoluta"
            elif ranking == 2:
                return_var = "Seconda classificata"
            elif ranking == 3:
                return_var = "Terza classificata"
            elif ranking == 4:
                return_var = "Quarta classificata"
            elif ranking == 5:
                return_var = "Quinta classificata"
        elif contest_type == project_constants.MAN_CONTEST:
            # check podium user ranking
            if ranking == 1:
                return_var = "Vincitore assoluto"
            elif ranking == 2:
                return_var = "Secondo classificato"
            elif ranking == 3:
                return_var = "Terzo classificato"
            elif ranking == 4:
                return_var = "Quarto classificato"
            elif ranking == 5:
                return_var = "Quinto classificato"

        return return_var
