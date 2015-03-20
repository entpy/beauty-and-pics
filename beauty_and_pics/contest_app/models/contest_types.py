from django.db import models

class Contest_Type(models.Model):
    id_contest_type = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    status = models.IntegerField()

    class Meta:
        app_label = 'contest_app'

    def __unicode__(self):
        return self.code

"""
	* id_contest_type (PK)
	* description
	* status (0 non attivo, 1 attivo)
"""
