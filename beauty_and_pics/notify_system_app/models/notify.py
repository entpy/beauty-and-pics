# -*- coding: utf-8 -*-

from django.db import models
from datetime import date
from dateutil.relativedelta import *
from website.exceptions import *
from beauty_and_pics.consts import project_constants
import sys, logging

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

# extends User model
class Notify(models.Model):
    id_notify = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=500, null=True)

    



    """
    user = models.OneToOneField(User, null=True)
    contest_type = models.ForeignKey(Contest_Type, null=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True)
    status = models.IntegerField(null=True)
    birthday_date = models.DateField(null=True)
    hair = models.CharField(max_length=15, null=True, blank=True)
    eyes = models.CharField(max_length=15, null=True, blank=True)
    height = models.CharField(max_length=4, null=True, blank=True)
    newsletters_bitmask = models.CharField(max_length=20, default=(project_constants.WEEKLY_REPORT_EMAIL_BITMASK + project_constants.CONTEST_REPORT_EMAIL_BITMASK), null=True)
    update_date = models.DateTimeField(auto_now=True)
    """

    class Meta:
        app_label = 'user_notify_system_app'
