from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    id_favorite = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    id_account_favorite = models.IntegerField()

    class Meta:
        app_label = 'account_app'

"""
        * id_favorite (PK)
        * user (FK)
        * id_account_favorite (FK)
"""
