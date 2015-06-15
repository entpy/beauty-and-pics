# -*- coding: utf-8 -*-

from django.db import models
from beauty_and_pics.consts import project_constants
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Contest_Type(models.Model):
    id_contest_type = models.AutoField(primary_key=True)
    code = models.CharField(max_length=25)
    description = models.CharField(max_length=150)
    status = models.IntegerField(max_length=1, default=0)

    class Meta:
        app_label = 'contest_app'

    def __unicode__(self):
        return self.code

    def get_contest_type_by_code(self, code=None):
        """Function to retrieve contest_types instance by code"""
        return_var = None
        if code:
            try:
                return_var = Contest_Type.objects.get(code=code)
            except Contest_Type.DoesNotExist:
                pass

        return return_var

    def get_contest_type_code_by_id(self, contest_type_id=None):
        """Function to retrieve contest type code form contest type id"""
        return_var = None
        if contest_type_id:
            try:
                contest_obj = Contest_Type.objects.get(pk=contest_type_id)
            except Contest_Type.DoesNotExist:
                pass
            else:
                return_var = contest_obj["code"]

        return return_var

    def create_default(self):
        """Function to create default contest types"""
        # create man-contest, if not exists
	try:
	    Contest_Type.objects.get(code=project_constants.MAN_CONTEST)
	except Contest_Type.DoesNotExist:
            Contest_Type_obj = Contest_Type(
                                    code = project_constants.MAN_CONTEST,
                                    description = "Contest maschile",
                                    status = 1,
                                )
            Contest_Type_obj.save()
            logger.info("contest_type creato: " + str(project_constants.MAN_CONTEST))

        # create woman-contest, if not exists
	try:
	    Contest_Type.objects.get(code=project_constants.WOMAN_CONTEST)
	except Contest_Type.DoesNotExist:
            Contest_Type_obj = Contest_Type(
                                    code = project_constants.WOMAN_CONTEST,
                                    description = "Contest femminile",
                                    status = 1,
                                )
            Contest_Type_obj.save()
            logger.info("contest_type creato: " + str(project_constants.WOMAN_CONTEST))

        return True

"""
	* id_contest_type (PK)
	* description
	* status (0 non attivo, 1 attivo)
"""
