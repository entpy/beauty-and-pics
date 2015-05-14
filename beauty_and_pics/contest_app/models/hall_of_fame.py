# -*- coding: utf-8 -*-

from django.db import models
from contest_app.models.contests import Contest
from django.contrib.auth.models import User
from beauty_and_pics.consts import project_constants
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class HallOfFame(models.Model):
    id_hall_of_fame = models.AutoField(primary_key=True)
    contest = models.ForeignKey('Contest')
    user = models.ForeignKey(User, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=75)
    profile_image = models.ImageField(max_length=500, null=True)
    ranking = models.IntegerField()
    points = models.IntegerField(max_length=50)

    class Meta:
        app_label = 'contest_app'

    def __unicode__(self):
        return str(self.id_hall_of_fame)

    """
        * id_hall_of_fame (PK)
        * contest (FK)
        * user (FK)
        * first_name
        * last_name
        * email
        * profile_image
        * ranking
        * points
    """

    def save_active_contest_hall_of_fame(self, contest_type=None):
        """Function to create hall of fame about a contest (before contest close action)"""
        from account_app.models.accounts import Account
        contest_obj = Contest()
        account_obj = Account()
        return_var = False
        if contest_type:
            # retrieve active contest
            active_contest = contest_obj.get_active_contests_by_type(contest_type=contest_type)
            # retrieve best 5 users about this contest
            top_users = account_obj.get_top_five_contest_user(contest_type=contest_type, hall_of_fame=True)
            if top_users:
                ranking = 1
                for single_user in top_users:
                    # save user inside hall of fame *.*
                    hall_of_fame_obj = HallOfFame()
                    hall_of_fame_obj.contest = active_contest
                    hall_of_fame_obj.user = single_user["user"]
                    hall_of_fame_obj.first_name = single_user["user_first_name"]
                    hall_of_fame_obj.last_name = single_user["user_last_name"]
                    hall_of_fame_obj.email = single_user["user_email"]
                    hall_of_fame_obj.profile_image = single_user["user_profile_image_url"]
                    hall_of_fame_obj.ranking = ranking
                    hall_of_fame_obj.points = single_user["user_total_points"]
                    hall_of_fame_obj.save()
                    ranking +=1
                    return_var = True

        return return_var

    def get_last_active_contest_hall_of_fame(self, contest_type=None):
        """Function to retrieve hall of fame about a contest (last active contest)"""
        contest_obj = Contest()
        return_var = None

        if contest_type:
            # retrieve last active contest
            last_active_contest = contest_obj.get_last_active_contests_by_type(contest_type=contest_type)
            if last_active_contest:
                # retrieve all hall of fame users about last active contest
                return_var = HallOfFame.objects.get(contest__contest_type__code=last_active_contest.contest_type.code).order_by('ranking')
                return_var["contest_year"] = contest_obj.get_contest_year(contest=last_active_contest)

        return return_var

    def get_last_active_contest_winner(self, contest_type=None):
        """Function to retrieve winner user about last active contest"""
        return_var = None

        if contest_type:
            return_var = self.get_last_active_contest_hall_of_fame(contest_type=contest_type)[0]

        return return_var

    # In futuro fare una pagina con l'elenco dei vincitori di tutti i contest
    def get_all_contests_hall_of_fame(self, contest_type=None):
        """Function to retrieve hall of fame about all contests"""
        return_var = True

        return return_var
