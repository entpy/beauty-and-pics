from django.db import models

class Metric(models.Model):
    id_metric = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'contest_app' 

"""
        * id_metric (PK)
        * name
"""
