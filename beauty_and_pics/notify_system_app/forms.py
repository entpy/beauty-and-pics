# -*- coding: utf-8 -*-

from django.forms import ModelForm
from notify_system_app.models import Notify

class NotifyForm(ModelForm):
    class Meta:
        model = Notify
        fields = ['title', 'message', 'action_url',]
