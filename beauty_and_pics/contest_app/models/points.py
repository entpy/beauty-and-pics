from django.db import models
from django.contrib.auth.models import User
from contest_app.models.contests import Contest

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
        return str(self.contest.id_contest_type.code) + " " + str(self.user.email)

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
