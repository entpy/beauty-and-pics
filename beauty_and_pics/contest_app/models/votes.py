# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from website.exceptions import *
from django.contrib.auth.models import User
from contest_app.models.contests import Contest
from contest_app.models.contest_types import Contest_Type
from contest_app.models.points import Point
from account_app.models.accounts import Account
from beauty_and_pics.consts import project_constants
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

    def __check_if_user_can_vote(self, user_id, ip_address):
        """Function to check if a user can (re-)vote a catwalker"""
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
            if not votation_data["face_vote_points"]:
                raise VoteMetricMissingError
            if not votation_data["look_vote_points"]:
                raise VoteMetricMissingError
            if int(votation_data["global_vote_points"]) < 1 or int(votation_data["global_vote_points"]) > 5:
                raise VoteMetricWrongValueError
            if int(votation_data["face_vote_points"]) < 1 or int(votation_data["face_vote_points"]) > 5:
                raise VoteMetricWrongValueError
            if int(votation_data["look_vote_points"]) < 1 or int(votation_data["look_vote_points"]) > 5:
                raise VoteMetricWrongValueError

        return True

    def __check_if_account_contest_is_active(self, user_id):
        """Function to check if contest about account is active"""
        # retrieving account contest code
        account_obj = Account()
        account_data = account_obj.custom_user_id_data(user_id=user_id)
        contest_obj = Contest()
        # TODO invece di account_data["gender"] -> account_data["contest_type"]
        if contest_obj.get_contests_type_status(contest_type=account_data["gender"]) != project_constants.CONTEST_ACTIVE:
            raise ContestNotActiveError

        return True

    def create_votation(self, user_id, ip_address):
        """Function to save if an account perform a votation"""
        if user_id and ip_address:
	    account_obj = Account()
            vote_obj = Vote()
            vote_obj.user = account_obj.get_user_about_id(user_id=user_id)
            vote_obj.ip_address = ip_address
            vote_obj.save()

        return True

    def perform_votation(self, votation_data, user_id, ip_address):
        """Function to perform a votation after validity check"""
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
            else:
                # check if user can vote
                try:
                    self.__check_if_user_can_vote(user_id=user_id, ip_address=ip_address)
                except UserAlreadyVotedError:
                    # send exception to parent try-except block
                    logger.error("Errore nella votazione, utente già votato | error code: " + str(UserAlreadyVotedError.get_error_code))
                    raise
                else:
                    # TODO: all seem right, perform votation
                    point_obj = Point()
                    # point_obj.add_points(points, metric_obj, user_obj, contest_obj)

                    # add points and "create_votation"
		    self.create_votation(user_id=user_id, ip_address=ip_address)
		    logger.debug("VOTAZIONE IN CORSO")
                    pass

        return True
