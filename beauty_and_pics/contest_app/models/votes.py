# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from website.exceptions import *
from django.contrib.auth.models import User
from contest_app.models.contest_types import Contest_Type
from contest_app.models.points import Point
from beauty_and_pics.consts import project_constants
from django.http import HttpResponse
import sys, logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Vote(models.Model):
    id_vote = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    ip_address = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'contest_app'

    """
            * id_vote (PK)
            * user (FK)
            * ip_address
            * date
    """

    def check_if_user_can_vote(self, user_id, ip_address, request):
        """Function to check if a user can (re-)vote a catwalker"""
        # check if exists cookie
        if request.COOKIES.get(project_constants.USER_ALREADY_VOTED_COOKIE_NAME + str(user_id)):
            raise UserAlreadyVotedError
        else:
            try:
                vote_obj = Vote.objects.get(user__id=user_id, ip_address=ip_address)
                # user already voted this catwalker, check if vote date is <
                # project_constants.SECONDS_BETWEEN_VOTATION user can't revote
                datediff = datetime.now() - vote_obj.date
                if datediff.total_seconds() < project_constants.SECONDS_BETWEEN_VOTATION:
                    # user can't re-vote, raise an exception
                    raise UserAlreadyVotedError
                else:
                    # user can (re-)vote this catwalker, remove user row from db table
                    vote_obj.delete()
            except Vote.DoesNotExist:
                # user can vote this catwalker
                pass

        return True

    def __check_if_votation_data_are_valid(self, votation_data=None):
        """Function to check if all votation data are valid"""
        if votation_data:
            if not votation_data["user_id"]:
                raise VoteUserIdMissingError
            if not votation_data["global_vote_points"]:
                raise VoteMetricMissingError
            if not votation_data["smile_vote_points"]:
                raise VoteMetricMissingError
            if not votation_data["look_vote_points"]:
                raise VoteMetricMissingError
            if int(votation_data["global_vote_points"]) < 1 or int(votation_data["global_vote_points"]) > 5:
                raise VoteMetricWrongValueError
            if int(votation_data["smile_vote_points"]) < 1 or int(votation_data["smile_vote_points"]) > 5:
                raise VoteMetricWrongValueError
            if int(votation_data["look_vote_points"]) < 1 or int(votation_data["look_vote_points"]) > 5:
                raise VoteMetricWrongValueError

        return True

    def __check_if_account_contest_is_active(self, user_id):
        """Function to check if contest about account is active"""
	from account_app.models.accounts import Account
	from contest_app.models.contests import Contest

        try:
            # retrieving account contest code
            account_obj = Account()
            account_data = account_obj.custom_user_id_data(user_id=user_id)
        except User.DoesNotExist:
            raise VoteUserIdMissingError
        else:
            contest_obj = Contest()
            if contest_obj.get_contests_type_status(contest_type=account_data["contest_type"]) != project_constants.CONTEST_ACTIVE:
                raise ContestNotActiveError

        return True

    def create_votation(self, user_id, ip_address):
        """Function to save if an account perform a votation"""
	from account_app.models.accounts import Account

        if user_id and ip_address:
            # save ip adress inside db
	    account_obj = Account()
            vote_obj = Vote()
            vote_obj.user = account_obj.get_user_about_id(user_id=user_id)
            vote_obj.ip_address = ip_address
            vote_obj.save()

        return True

    def perform_votation(self, votation_data, user_id, ip_address, request):
        """Function to perform a votation after validity check"""
	from account_app.models.accounts import Account
	from contest_app.models.contests import Contest
	from contest_app.models.metrics import Metric

        return_var = False
        try:
            self.__check_if_votation_data_are_valid(votation_data=votation_data)
        except VoteUserIdMissingError:
            # send exception to parent try-except block
            logger.error("Errore nella votazione, user_id non presente | error code: " + str(VoteUserIdMissingError.get_error_code))
            raise
        except VoteMetricMissingError:
            # send exception to parent try-except block
            logger.error("Errore nella votazione, una o più metriche non presenti | error code: " + str(VoteMetricMissingError.get_error_code))
            raise
        except VoteMetricWrongValueError:
            # send exception to parent try-except block
            logger.error("Errore nella votazione, metriche con valore non compreso tra 1 e 5 | error code: " + str(VoteMetricWrongValueError.get_error_code))
            raise
        else:
            # check if contest is active
            try:
                self.__check_if_account_contest_is_active(user_id=user_id)
            except ContestNotActiveError:
                # send exception to parent try-except block
                logger.error("Errore nella votazione, contest non attivo | error code: " + str(ContestNotActiveError.get_error_code))
                raise
            except VoteUserIdMissingError:
                # send exception to parent try-except block
                logger.error("Errore nella votazione, user_id non presente | error code: " + str(VoteUserIdMissingError.get_error_code))
                raise
            else:
                # check if user can vote
                try:
                    self.check_if_user_can_vote(user_id=user_id, ip_address=ip_address, request=request)
                except UserAlreadyVotedError:
                    # send exception to parent try-except block
                    logger.error("Errore nella votazione, utente già votato | error code: " + str(UserAlreadyVotedError.get_error_code))
                    raise
                else:
                    # all seem right, perform votation
		    account_obj = Account()
		    contest_obj = Contest()
		    metric_obj = Metric()

		    # load vote data
		    global_metric_instance = metric_obj.get_metric_by_name(name=project_constants.VOTE_METRICS_LIST["global_metric"])
		    smile_metric_instance = metric_obj.get_metric_by_name(name=project_constants.VOTE_METRICS_LIST["smile_metric"])
		    look_metric_instance = metric_obj.get_metric_by_name(name=project_constants.VOTE_METRICS_LIST["look_metric"])
		    user_instance = account_obj.get_user_about_id(user_id=votation_data["user_id"])
		    contest_instance = contest_obj.get_active_contests_by_type(contest_type=user_instance.account.contest_type)

		    # perform vote
                    point_obj = Point()
		    # global metric vote
                    point_obj.add_points(points=votation_data["global_vote_points"], metric_obj=global_metric_instance, user_obj=user_instance, contest_obj=contest_instance)
		    # smile metric vote
                    point_obj.add_points(points=votation_data["smile_vote_points"], metric_obj=smile_metric_instance, user_obj=user_instance, contest_obj=contest_instance)
		    # look metric vote
                    point_obj.add_points(points=votation_data["look_vote_points"], metric_obj=look_metric_instance, user_obj=user_instance, contest_obj=contest_instance)

                    # saving that user voted this catwalker
		    self.create_votation(user_id=user_id, ip_address=ip_address)
		    logger.debug("VOTAZIONE EFFETTUATA da " + str(ip_address) + " (" + str(request.META.get('HTTP_USER_AGENT', '')) + ") per " + str(user_instance.email) + " (" + str(user_instance.id) + ")")
                    pass

        return True
