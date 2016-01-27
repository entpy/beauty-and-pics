# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from website.exceptions import *
from django.contrib.auth.models import User
from contest_app.models.contest_types import Contest_Type
from contest_app.models.points import Point
from beauty_and_pics.common_utils import CommonUtils
from beauty_and_pics.consts import project_constants
from django.http import HttpResponse
import sys, logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Vote(models.Model):
    id_vote = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(User, default=None, related_name='from_user')
    to_user = models.ForeignKey(User, default=None, related_name='to_user')
    ip_address = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'contest_app'

    """
            * id_vote (PK)
            * from_user (FK)
            * to_user (FK)
            * ip_address
            * date
    """

    # controllo che il from_user_id abbia la mail verificata
    def check_if_user_can_vote(self, from_user_id, to_user_id, request):
        """
        Function to check if a user can (re-)vote another user
        1) controllo il cookie
        2) controllo data ultima votazione
        """

        # 1) controllo il cookie
        if request.COOKIES.get(project_constants.USER_ALREADY_VOTED_COOKIE_NAME + str(to_user_id)):
            raise UserAlreadyVotedError
        try:
            vote_obj = Vote.objects.get(from_user__id=from_user_id, to_user__id=to_user_id)
            # 2) controllo data ultima votazione
            # user already voted this catwalker, if vote date is < project_constants.SECONDS_BETWEEN_VOTATION
            # user can't revote
            datediff = datetime.now() - vote_obj.date
            logger.debug("datetime.now: " + str(datetime.now()))
            logger.debug("vote date: " + str(vote_obj.date))
            logger.debug("seconds: " + str(datediff.total_seconds()))
            if datediff.total_seconds() < project_constants.SECONDS_BETWEEN_VOTATION:
                # user can't re-vote, raise an exception
                raise UserAlreadyVotedError
            else:
                # user can revote this catwalker, remove user row from db table
                vote_obj.delete()
        except Vote.DoesNotExist:
            # user can vote this catwalker
            pass

        return True

    def perform_votation(self, from_user_id, to_user_id, vote_code, request):
        """
            Function to perform a votation after validity check.
            Exceptions:
            - PerformVotationDataMissingError
            - PerformVotationVoteCodeDataError
            - PerformVotationFromUserMissingError
            - PerformVotationToUserMissingError
            - PerformVotationUserContestMissingError
        """
	from account_app.models.accounts import Account
	from contest_app.models.contests import Contest
	Account_obj = Account()
        CommonUtils_obj = CommonUtils()

        # controllo che il vote_code sia esistente, altrimenti non faccio nulla
        if not from_user_id or not to_user_id or not vote_code or not request:
            raise PerformVotationDataMissingError

        vote_code_data = self.get_single_vote_code_data(vote_code=vote_code)
        if not vote_code_data:
            raise PerformVotationVoteCodeDataError

        # qualche get per ottenere gli oggetti
        try:
            FromUser_obj = Account_obj.get_user_about_id(user_id=from_user_id)
        except User.DoesNotExist:
            raise PerformVotationFromUserMissingError
        try:
            ToUser_obj = Account_obj.get_user_about_id(user_id=to_user_id)
        except User.DoesNotExist:
            raise PerformVotationToUserMissingError

        try:
            # insert points metrics
            self.insert_votation_points(vote_code_data=vote_code_data, from_user_obj=FromUser_obj, to_user_obj=ToUser_obj)
        except PerformVotationUserContestMissingError:
            raise

        # insert row in votes (per non permettere più il voto di questo utente)
        self.insert_vote(from_user_obj=FromUser_obj, to_user_obj=ToUser_obj, request=request)

        # some debug info
        client_ip_address = CommonUtils_obj.get_ip_address(request=request)
        logger.debug("##nuova votazione##")
        logger.debug("utente votato: " + str(ToUser_obj.email) + " (id: " + str(ToUser_obj.id) + ")")
        logger.debug("votato da: " + str(FromUser_obj.email) + " (id: " + str(FromUser_obj.id) + ")")
        logger.debug("codice di voto: " + str(vote_code))
        logger.debug("indirizzo IP del votante: " + str(client_ip_address))

        return True

    def insert_votation_points(self, vote_code_data, from_user_obj, to_user_obj):
        """Function to insert points for every metric"""
	from contest_app.models.contests import Contest
	from contest_app.models.metrics import Metric
	Contest_obj = Contest()
	Metric_obj = Metric()

        # retrieve to_user contest_obj
        ToUserContest_obj = Contest_obj.get_active_contests_by_type(contest_type=to_user_obj.account.contest_type)
        if not ToUserContest_obj:
            raise PerformVotationUserContestMissingError

        # retrieve metrics obj
        SmileMetric_obj = Metric_obj.get_metric_by_name(name=project_constants.VOTE_METRICS_LIST["smile_metric"])
        LookMetric_obj = Metric_obj.get_metric_by_name(name=project_constants.VOTE_METRICS_LIST["look_metric"])
        GlobalMetric_obj = Metric_obj.get_metric_by_name(name=project_constants.VOTE_METRICS_LIST["global_metric"])
        StyleMetric_obj = Metric_obj.get_metric_by_name(name=project_constants.VOTE_METRICS_LIST["style_metric"])

        # inserisco i punteggi per ogni metrica
        Point_obj = Point()
        Point_obj.add_points(points=vote_code_data["points"][project_constants.VOTE_METRICS_LIST["smile_metric"]], metric_obj=SmileMetric_obj, user_obj=to_user_obj, contest_obj=ToUserContest_obj)
        Point_obj.add_points(points=vote_code_data["points"][project_constants.VOTE_METRICS_LIST["look_metric"]], metric_obj=LookMetric_obj, user_obj=to_user_obj, contest_obj=ToUserContest_obj)
        Point_obj.add_points(points=vote_code_data["points"][project_constants.VOTE_METRICS_LIST["global_metric"]], metric_obj=GlobalMetric_obj, user_obj=to_user_obj, contest_obj=ToUserContest_obj)
        Point_obj.add_points(points=vote_code_data["points"][project_constants.VOTE_METRICS_LIST["style_metric"]], metric_obj=StyleMetric_obj, user_obj=to_user_obj, contest_obj=ToUserContest_obj)

        return True

    def insert_vote(self, from_user_obj, to_user_obj, request):
        """Function to save a user votation"""
        # retrieve ip address
        CommonUtils_obj = CommonUtils()
        client_ip_address = CommonUtils_obj.get_ip_address(request=request)

        # save votation
        vote_obj = Vote()
        vote_obj.from_user = from_user_obj
        vote_obj.to_user = to_user_obj
        vote_obj.ip_address = client_ip_address
        vote_obj.save()

        return True

    def get_single_vote_code_data(self, vote_code):
        """Function to retrieve all info about a single 'vote_code'"""
        return_var = False
        all_votes_data = self.get_all_vote_codes_data()
        single_vote_code_data = all_votes_data.get(vote_code)

        if single_vote_code_data:
            return_var = single_vote_code_data

        return return_var

    def get_all_vote_codes_data(self):
        """
        Function to retrieve all info about all vote codes

        ###vote_code(sorriso, sguardo, globale, stile)###
        sguardo_ammaliante(2,8,3,2)
        persona_solare(8,2,2,3)
        troppo_stile(3,2,3,7)
        che_classe(2,2,8,3)
        impeccabile(4,4,3,4)
        notevole(4,4,4,3)
        """
        return_var = {
            'sguardo_ammaliante' : {
                'label' : 'Sguardo ammaliante',
                'points' : {
                    project_constants.VOTE_METRICS_LIST['smile_metric'] : '2',
                    project_constants.VOTE_METRICS_LIST['look_metric'] : '8',
                    project_constants.VOTE_METRICS_LIST['global_metric'] : '3',
                    project_constants.VOTE_METRICS_LIST['style_metric'] : '2'
                }
            },
            'persona_solare' : {
                'label' : 'Persona solare',
                'points' : {
                    project_constants.VOTE_METRICS_LIST['smile_metric'] : '8',
                    project_constants.VOTE_METRICS_LIST['look_metric'] : '2',
                    project_constants.VOTE_METRICS_LIST['global_metric'] : '2',
                    project_constants.VOTE_METRICS_LIST['style_metric'] : '3'
                }
            },
            'troppo_stile' : {
                'label' : 'Troppo stile',
                'points' : {
                    project_constants.VOTE_METRICS_LIST['smile_metric'] : '3',
                    project_constants.VOTE_METRICS_LIST['look_metric'] : '2',
                    project_constants.VOTE_METRICS_LIST['global_metric'] : '3',
                    project_constants.VOTE_METRICS_LIST['style_metric'] : '7'
                }
            },
            'che_classe' : {
                'label' : 'Che classe',
                'points' : {
                    project_constants.VOTE_METRICS_LIST['smile_metric'] : '2',
                    project_constants.VOTE_METRICS_LIST['look_metric'] : '2',
                    project_constants.VOTE_METRICS_LIST['global_metric'] : '8',
                    project_constants.VOTE_METRICS_LIST['style_metric'] : '3'
                }
            },
            'impeccabile' : {
                'label' : 'Impeccabile',
                'points' : {
                    project_constants.VOTE_METRICS_LIST['smile_metric'] : '4',
                    project_constants.VOTE_METRICS_LIST['look_metric'] : '4',
                    project_constants.VOTE_METRICS_LIST['global_metric'] : '3',
                    project_constants.VOTE_METRICS_LIST['style_metric'] : '4'
                }
            },
            'notevole' : {
                'label' : 'Notevole',
                'points' : {
                    project_constants.VOTE_METRICS_LIST['smile_metric'] : '4',
                    project_constants.VOTE_METRICS_LIST['look_metric'] : '4',
                    project_constants.VOTE_METRICS_LIST['global_metric'] : '4',
                    project_constants.VOTE_METRICS_LIST['style_metric'] : '3'
                }
            }
        }

        return return_var
