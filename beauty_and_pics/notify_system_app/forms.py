# -*- coding: utf-8 -*-

from django.forms import ModelForm
from notify_system_app.models import Notify
import sys

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

class NotifyForm(ModelForm):
    class Meta:
        model = Notify
        fields = ['title', 'message', 'action_title', 'action_url',]
