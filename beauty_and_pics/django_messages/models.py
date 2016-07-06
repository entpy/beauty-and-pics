# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Conversation(models.Model):
    id_conversation = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now=True) # la data di creazione della conversazione

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_conversation) + " - " + str(self.title)

    def get_conversation(self, id_conversation):
        """Function to retrieve a conversation instance"""
        return_var = None
        try:
            return_var = Conversation.objects.get(pk=id_conversation)
        except Conversation.DoesNotExist:
            raise

        return return_var

    def create_conversation(self, title=None):
        """Function to create a new conversation between two users"""
        return_var = None

        Conversation_obj = Conversation()
        if title:
            Conversation_obj.title = title

        if Conversation_obj.save():
            return_var = Conversation_obj

        return return_var


class Participant(models.Model):
    id_participant = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation)
    user = models.ForeignKey(User) # partecipante della conversazione
    is_master = models.IntegerField(default=0) # se = 1 è il creatore della conversazione
    join_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_participant)

    def add_participant(self, user_id, conversation_id, is_master=False):
        """Function to add a participant"""
        return_var = None

        if user_id and conversation_id:
            Participant_obj = Participant()
            Participant_obj.conversation_id = conversation_id
            Participant_obj.user_id = user_id
            Participant_obj.is_master = is_master
            return_var = Participant_obj.save()

        return return_var

    def remove_participant(self, user_id, conversation_id):
        """Function to remove a participant"""
        return_var = None

        return return_var

    def get_participant(self, user_id, conversation_id):
        """Function to retrieve a participant instance"""
        return_var = None

        try:
            return_var = Participant.objects.get(user_id=user_id, conversation_id=conversation_id)
        except Participant.DoesNotExist:
            raise

        return return_var


class MessageRead(models.Model):
    id_message_read = models.AutoField(primary_key=True)
    message = models.ForeignKey(Message)
    participant = models.ForeignKey(Participant)
    read_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_message_read)


class Message(models.Model):
    id_message = models.AutoField(primary_key=True)
    participant = models.ForeignKey(Participant)
    text = models.TextField() # testo del messaggio
    write_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_message)

    def write_message(self, user_id, conversation_id, text):
        """Function to write a new message into a conversation"""
        return_var = False
        Participant_obj = Participant()

        if user_id and conversation_id and text:
            Message_obj = Message()
            # retrieve participant instance
            Message_obj.participant_id = Participant_obj.get_participant(user_id=user_id, conversation_id=conversation_id)
            Message_obj.text = text
            return_var = Message_obj.save()

        return return_var

    def get_conversation_messages(self, user_id1, user_id2):
        """Function to retrieve all conversation messages about two users"""
        return_var = None

        if user_id1 and user_id2:
            return_var = list(Message.objects.values(
                'conversation__sender__id',
                'conversation__sender__first_name',
                'conversation__sender__last_name',
                'conversation__recipient__id',
                'conversation__recipient__first_name',
                'conversation__recipient__last_name',
                'message',
                'write_date'
            ).filter(
                Q('sender__id=' + user_id) | Q('recipient__id=' + recipient_id)
            ).order_by('-write_date'))

        return return_var

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
