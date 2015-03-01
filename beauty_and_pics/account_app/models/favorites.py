from django.db import models

class Favorite(models.Model):
    id_favorite = models.IntegerField(primary_key=True)
    id_account = models.ForeignKey('Account')
    id_account_favorite = models.ForeignKey('Account')

    class Meta:
        app_label = 'website' 

"""
        * id_favorite (PK)
        * id_account (FK)
        * id_account_favorite (FK)
"""
