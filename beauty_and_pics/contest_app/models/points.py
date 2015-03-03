from django.db import models
from account_app.models.accounts import Account

class Point(models.Model):
    id_point = models.IntegerField(primary_key=True)
    id_contest = models.ForeignKey('Contest')
    id_account = models.ForeignKey(Account)
    id_metric = models.ForeignKey('Metric')
    date = models.DateField()
    points = models.IntegerField()

    class Meta:
        app_label = 'contest_app' 

"""
	* id_point (PK)
	* id_contest (FK)
	* id_account (FK)
	* id_metric (FK)
	* date
	* points
"""