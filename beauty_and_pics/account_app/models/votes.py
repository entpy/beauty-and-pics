from django.db import models

class Vote(models.Model):
    id_vote = models.IntegerField(primary_key=True)
    account = models.ForeignKey('Account')
    ip_address = models.CharField(max_length=50)
    date = models.DateField()

    class Meta:
        app_label = 'website' 

"""
        * id_vote (PK)
        * id_account (FK)
        * ip_address
        * date
"""
