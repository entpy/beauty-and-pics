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
        return str(self.id_conversation)

    def get_conversation(self, user_id1, user_id2):
        """Function to retrieve a conversation instance"""
        return_var = None

        try:
            return_var = Conversation.objects.get(Q('sender__id=' + user_id1, 'recipient__id=' + user_id2) | Q('sender__id=' + user_id2, 'recipient__id=' + user_id1))
        except Conversation.DoesNotExist:
            raise

        return return_var

    def create_conversation(self, sender_id, recipient_id):
        """Function to create a new conversation between two users"""
        return_var = None

        Conversation_obj = Conversation()
        Conversation_obj.sender_id = sender_id
        Conversation_obj.recipient_id = recipient_id
        if Conversation_obj.save():
            return_var = Conversation_obj

        return return_var

    def get_user_conversations(self, user_id):
        """Function to retrieve a conversation list about a user (in genere
        l'utente loggato)"""
        return_var = None

        return list(Conversation.objects.values('sender__id', 'recipient__id').filter(Q('sender__id=' + user_id) | Q('recipient__id=' + recipient_id)))


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


class BlockList(models.Model):
    id_block_list = models.AutoField(primary_key=True)

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_block_list)


class Message(models.Model):
    id_message = models.AutoField(primary_key=True)
    participant = models.ForeignKey(Participant)
    text = models.TextField() # testo del messaggio
    write_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_message)

    def add_message_to_conversation(self, sender_id, recipient_id, message):
        """Function to add a message to a conversation between two users"""
        return_var = False
        Conversation_obj = Conversation()
        UserBlock_obj = UserBlock()
        Message_obj = Message()

        # prelevo la conversazione tra i due (non so chi tra i due sia il
        # mittente e chi il destinatario)
        try:
            Message_obj.conversation = Conversation_obj.get_conversation(user_id1=sender_id , user_id2=recipient_id)
        except Conversation.DoesNotExist:
            # la conversazione tra i due non esiste, quindi la creo
            Message_obj.conversation = Conversation_obj.create_conversation(sender_id=sender_id, recipient_id=recipient_id)

        # controllo che il destinatario non abbia bloccato il mittente
        if UserBlock_obj.check_if_user_is_blocked(user_id=recipient_id, user_blocked_id=sender_id):
            # il mittente è stato bloccato
            Message_obj.sender_is_blocked = 1

        Message_obj.message = message
        if Message_obj.save():
            return_var = True

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


class UserBlock(models.Model):
    id_user_block = models.AutoField(primary_key=True)
    user = models.ForeignKey(User) # l'utente che ha bloccato
    user_blocked = models.ForeignKey(User) # l'utente che è stato bloccato
    date = models.DateTimeField(auto_now=True) # la data in cui è avvenuto il blocco

    class Meta:
        app_label = 'django_messages'

    def __unicode__(self):
        return str(self.id_user_blocked)

    def block_user(self, user_id, user_blocked_id):
        """Function to block a user"""
        return_var = False
        UserBlock_obj = UserBlock()

        UserBlock_obj.user_id = user_id
        UserBlock_obj.user_blocked_id = user_blocked_id
        if UserBlock_obj.save():
            return_var = True

        return return_var

    def unblock_user(self, user_id, user_blocked_id):
        """Function to un-block a user"""
        if UserBlock.objects.filter('user__id=' + user_id, 'user_blocked__id=' + user_blocked_id).delete()

        return True

    def check_if_user_is_blocked(self, user_id, user_blocked_id):
        """Function to check if a user is blocked"""
        return_var = False

        if UserBlock.objects.filter('user__id=' + user_id, 'user_blocked__id=' + user_blocked_id).exists():
            return_var = True

        return return_var

    def show_unblocked_recipients(self):
        """Function to show all unblocked recipients"""

        return True
