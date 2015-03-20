from django.db import models

class Metric(models.Model):
    id_metric = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'contest_app'

    def __unicode__(self):
        return str(self.name)

"""
        * id_metric (PK)
        * name
"""
