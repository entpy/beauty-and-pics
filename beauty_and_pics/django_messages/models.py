# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from contest_app.models.contest_types import Contest_Type
from contest_app.models.metrics import Metric
from beauty_and_pics.consts import project_constants
from website.exceptions import ContestClosedNotExistsError
import logging, time

"""
        * id_contest (PK)
        * contest_type
        * start_date
        * end_date
        * status (0 in attesa di apertura, 1 attivo, 2 chiuso)
"""

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Message(models.Model):
    id_message = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room)
    user_room = models.ForeignKey(UserRoom)
    text = RichTextField()
    creation_date = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1) # 0 il msg è stato bannato

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_message)

class Room(models.Model):
    id_room = models.AutoField(primary_key=True)
    room_admin = models.ForeignKey(User)
    name = models.CharField(max_length=200, null=True, blank=True)
    is_public = models.IntegerField(default=0) # 
    creation_date = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1) # 0 la room è stata bannata e non è più possibile accedervi

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_room)

class MessageUserRoom(models.Model):
    id_message_user_room = models.AutoField(primary_key=True)
    message = models.ForeignKey(Message)
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room)
    read_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_room)

class UserRoom(models.Model):
    id_user_room = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room)
    enter_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_room)
