# -*- coding: utf-8 -*-

from django.db import models
from contest_app.models.contests import Contest
from django.contrib.auth.models import User
from account_app.models.images import Book
from beauty_and_pics.consts import project_constants
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class HallOfFame(models.Model):
    id_hall_of_fame = models.AutoField(primary_key=True)
    contest = models.ForeignKey('Contest')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    ranking = models.IntegerField()
    points = models.IntegerField()

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

    """
    def get_last_active_contest_hall_of_fame(self, contest_type, only_winner=False):
        ""Function to retrieve hall of fame about a contest (last active contest)""
        contest_obj = Contest()
        return_var = None

        # retrieve last active contest
        last_closed_contest = contest_obj.get_last_closed_contests_by_type(contest_type=contest_type)
        if last_closed_contest:
            # retrieve all hall of fame users about last active contest
            hall_of_fame_users = HallOfFame.objects.values(
                    'contest__start_date',
                    'user__id',
                    'user__first_name',
                    'user__last_name',
                    'ranking',
                    'points',
                    ).filter(contest__id_contest=last_closed_contest.id_contest).order_by('ranking')
	    if hall_of_fame_users:
		if only_winner:
		    # retrieve only winner
		    return_var = hall_of_fame_users[0]
		else:
		    # retrieve all top 100
		    return_var = hall_of_fame_users

        return return_var
    """

    def get_last_active_contest_winner(self, contest_type):
        """Function to retrieve winner user about last active contest"""
        Book_obj = Book()
        return_var = self.get_contest_top_100(contest_type=contest_type, contest_year=False, only_winner=True)
	if return_var:
	    return_var["profile_image"] = Book_obj.get_profile_thumbnail_image_url(user_id=return_var["user__id"])
	    return_var["profile_thumbnail_image"] = Book_obj.get_profile_image_url(user_id=return_var["user__id"])

        return return_var

    # TODO: testare elenco utenti per contest e anno.
    # testare anche utente vincitore
    def get_contest_top_100(self, contest_type, contest_year=False, only_winner=False):
        """Function to retrieve top 100 users about a contest"""
        Contest_obj = Contest()
        return_var = None

	# filter contest_type
	return_var = HallOfFame.objects.values(
		'contest__start_date',
		'user__id',
		'user__first_name',
		'user__last_name',
		'ranking',
		'points',
		).filter(contest__contest_type__code=contest_type)

	# filter year if specified
	if contest_year:
	    return_var = return_var.filter(contest__start_date__year=contest_year)
	else:
	    # se non ho specificato l'anno, mi baso sull'ultimo contest chiuso
	    last_closed_contest = Contest_obj.get_last_closed_contests_by_type(contest_type=contest_type)
	    return_var = return_var.filter(contest__id_contest=last_closed_contest.id_contest)

	# order by ranking
	return_var = return_var.order_by('ranking')

        # check if return only winner user
        if return_var and only_winner:
            return_var = return_var[0]

        return list(return_var)
