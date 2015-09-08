# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
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

class Notify(models.Model):

    # notify type selection
    NOTIFY_EMAIL = 1
    NOTIFY_WEBPUSH = 2
    NOTIFY_TYPE = ((NOTIFY_EMAIL, 'Notify via email'), (NOTIFY_WEBPUSH, 'Notify via webpush'),)

    notify_id = models.AutoField(primary_key=True)
    type = models.IntegerField(choices=NOTIFY_TYPE, default=NOTIFY_WEBPUSH)
    creation_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    action_url = models.CharField(max_length=100, null=True)

    class Meta:
        app_label = 'notify_system_app'

    def __unicode__(self):
        return str(self.title)

    # function to create a notify
    def create_notify(self, data):
        return True

    # function to send a notify to a recipents list
    def send_notify_via_mail(self, notify_id, recipients_list):
        return True

    # function to mark a notify as read
    def mark_notify_as_read(self, notify_id, user_id):
        return True

    # function to count notify not read about a user
    def count_notify_to_read(self, user_id):
        return True

    # function to retrieve info (title, description, ecc...) about a notify id
    def get_notify_info(self, notify_id):
        return True

    # function to retrieve a list of notify about a user
    def user_notify_list(self, filters, user_id):
        return True

"""
# la notifica può essere inviata via mail o vista solo sul sito (tipo push)
class Notify_Type(models.Model):
    notify_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, null=True)

    class Meta:
        app_label = 'notify_system_app'

    def __unicode__(self):
        return str(self.description)
"""

# se è presente una riga qua, la notifica è stata letta dall'utente
# valido solo per le notifiche sul sito
class User_Notify(models.Model):
    user_notify_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    notify = models.ForeignKey(Notify)
    read_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'notify_system_app'

    def __unicode__(self):
        return str(self.user_notify_id)
