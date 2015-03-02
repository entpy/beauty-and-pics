from django.db import models

class Favorite(models.Model):
    id_favorite = models.IntegerField(primary_key=True)
    id_account = models.ForeignKey('Account')
    id_account_favorite = models.IntegerField()

    class Meta:
        app_label = 'account_app' 

"""
        * id_favorite (PK)
        * id_account (FK)
        * id_account_favorite (FK)
"""
