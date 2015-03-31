from django.db import models
from account_app.models.accounts import Account
from contest_app.models.contests import Contest

class Point(models.Model):
    id_point = models.AutoField(primary_key=True)
    id_contest = models.ForeignKey('Contest')
    id_account = models.ForeignKey(Account)
    id_metric = models.ForeignKey('Metric')
    date = models.DateTimeField(auto_now=True)
    points = models.IntegerField()

    class Meta:
        app_label = 'contest_app'

    def __unicode__(self):
        return str(self.id_contest.id_contest_type.code) + " " + str(self.id_account.user.email)

    """
            * id_point (PK)
            * id_contest (FK)
            * id_account (FK)
            * id_metric (FK)
            * date
            * points
    """

    def add_points(self, points, metric_obj, account_obj, contest_obj):
        """Function to add points to a metric"""
        return_var = False
        if points and metric_obj and account_obj and contest_obj:
            # add points
            point_obj = Point()
            point_obj.id_contest = contest_obj
            point_obj.id_account = account_obj
            point_obj.id_metric = metric_obj
            point_obj.points = points
            point_obj.save()
            return_var = True

        return return_var
