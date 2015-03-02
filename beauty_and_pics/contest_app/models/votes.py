from django.db import models
from account_app.models.accounts import Account

class Vote(models.Model):
    id_vote = models.IntegerField(primary_key=True)
    id_account = models.ForeignKey(Account)
    ip_address = models.CharField(max_length=50)
    date = models.DateField()

    class Meta:
        app_label = 'contest_app' 

"""
        * id_vote (PK)
        * id_account (FK)
        * ip_address
        * date
"""
