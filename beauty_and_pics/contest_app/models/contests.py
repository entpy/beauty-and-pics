from django.db import models

class Contest(models.Model):
    id_contest = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    status = models.IntegerField()

    class Meta:
        app_label = 'contest_app'

"""
	* id_contest (PK)
	* start_date
	* end_date
	* name
	* description
	* status (0 in attesa di apertura, 1 attivo, 2 chiuso)
"""
