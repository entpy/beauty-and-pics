# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Count, Sum
from contest_app.models.contests import Contest
from beauty_and_pics.consts import project_constants
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Point(models.Model):
    id_point = models.AutoField(primary_key=True)
    contest = models.ForeignKey('Contest')
    user = models.ForeignKey(User)
    metric = models.ForeignKey('Metric')
    date = models.DateTimeField(auto_now=True)
    points = models.IntegerField()

    class Meta:
        app_label = 'contest_app'

    def __unicode__(self):
        return str(self.contest.contest_type.code) + " " + str(self.user.email)

    """
            * id_point (PK)
            * contest (FK)
            * user (FK)
            * metric (FK)
            * date
            * points
    """

    def add_points(self, points, metric_obj, user_obj, contest_obj):
        """Function to add points to a metric"""
        return_var = False
        if points and metric_obj and user_obj and contest_obj:
            logger.debug("##inserimento punti##")
            logger.debug("points: " + str(points))
            logger.debug("metric_obj: " + str(metric_obj))
            logger.debug("user_obj: " + str(user_obj))
            logger.debug("contest_obj: " + str(contest_obj))
            # add points
            point_obj = Point()
            point_obj.contest = contest_obj
            point_obj.user = user_obj
            point_obj.metric = metric_obj
            point_obj.points = points
            point_obj.save()
            return_var = True

        return return_var

    def get_single_user_contest_info(self, user_id=None):
        """Function to retrieve a dictionary with account contest info
        {
            'total_points': 39,
            u'global': {'total_points': 9, 'total_votes': 5},
            u'look': {'total_points': 13, 'total_votes': 5},
            u'smile': {'total_points': 17, 'total_votes': 5}
        }
        """

        # retrieve info 
	return Point.objects.values('metric__name').filter(user__id=user_id, contest__contest_type=F('user__account__contest_type'), contest__status=project_constants.CONTEST_ACTIVE).annotate(total_points=Sum('points'), total_votes = Count('points'))

    # TODO: implement this
    def get_user_position(self, user_id=None):
        """Function to retrieve the current user ranking"""
        return_var = False

        return return_var
