from django.db import models
from beauty_and_pics.consts import project_constants

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

    def __create_default_metrics(self):
        """Function to create default metrics"""
        for default_metric in project_constants.VOTE_METRICS_LIST:
            metric_obj = Metric(name=project_constants.VOTE_METRICS_LIST[default_metric])
            metric_obj.save()

        return True

    def __check_default_metrics_exist(self):
        """Function to check if default metrics exist"""
        return_var = False
        if Metric.objects.count():
            # default metrics exists
            return_var = True

        return return_var

    def metrics_manager(self):
        """Function to manage default metrics (create metrics if not already exist)"""
        return_var = False
        # check if default metrics already exist
        if not self.__check_default_metrics_exist():
            # default metrics must be created
            self.__create_default_metrics()
            return_var = True

        return return_var

    def get_metric_by_name(self, name):
	"""Function to retrieve a metric instance by name"""
	return_var = None
	try:
	    return_var = Metric.objects.get(name=name)
	except Metric.DoesNotExist:
	    return_var = False

	return return_var

