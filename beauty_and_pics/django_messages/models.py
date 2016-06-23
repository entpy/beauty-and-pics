# -*- coding: utf-8 -*-

from django.db import models
from datetime import timedelta
from django.utils import timezone
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Message(models.Model):
    id_message = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User) # mittente del messaggio
    recipient = models.ForeignKey(User) # destinatario del messaggio
    text = models.TextField() # testo del messaggio
    write_date = models.DateTimeField(auto_now=True)
    read_date = models.DateTimeField(null=True, blank=True) # se non settato il messaggio non è stato letto
    sender_deleted_at = models.DateTimeField("cancellato dal mittente il", null=True, blank=True)
    recipient_deleted_at = models.DateTimeField("cancellato dal destinatario il", null=True, blank=True)
    sender_is_blocked = models.IntegerField(default=0) # se 1 il mittente del messaggio è bloccato (quindi il messaggio non deve essere visibile al destinatario)

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_message)

    def write_message(self, sender_id, recipient_id, text):
        """Function to write a new message"""
        UserBlock_obj = UserBlock()
        Message_obj = Message()

        # controllo se il destinatario ha bloccato il mittente
        if UserBlock_obj.check_if_user_is_blocked(user_id=recipient_id, user_blocked_id=sender_id):
            # il mittente è stato bloccato
            Message_obj.sender_is_blocked = 1

        Message_obj.sender_id = sender_id
        Message_obj.recipient_id = recipient_id
        Message_obj.text = text
        Message_obj.save()

        return True

    def read_messages(self, sender_id, recipient_id):
        """
            Function to set all unread messages to read (a tutti quelli che non
            hanno una data di lettura e che non hanno sender_is_blocked ne imposto una)
        """

        return True

    def delete_sender_messages(self, sender_id, recipient_id):
        """
            Function delete all sender messages (setto la data di sender_deleted_at
            per tutti quelli che non ce l'hanno settata)
        """

        return True

    def delete_recipient_messages(self, sender_id, recipient_id):
        """
            Function delete all recipients messages (setto la data di recipient_deleted_at
            per tutti quelli che non ce l'hanno settata)
        """

        return True

    def count_unread_messages(self, recipient_id):
        """Function to count all unread messages about a recipient, it they
        have read_date unset"""

        return True

    def get_messages_about_sender(self, sender_id):
        """
            Function to retrieve all undeleted and 
            unblocked (sender_is_blocked = 0) message about a sender
        """

        return True


class UserBlock(models.Model):
    id_user_block = models.AutoField(primary_key=True)
    user = models.ForeignKey(User) # l'utente che ha bloccato
    user_blocked = models.ForeignKey(User) # l'utente che è stato bloccato
    date = models.DateTimeField(auto_now=True) # la data in cui è avvenuto il blocco


    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_user_blocked)

    def block_user(self):
        """Function to block a user"""

        return True

    def unblock_user(self):
        """Function to block a user"""

        return True

    def check_if_user_is_blocked(self, user_id, user_blocked_id):
        """Function to check if a user is blocked"""

        return True

    def show_unblocked_recipients(self):
        """Function to show all unblocked recipients"""

        return True
