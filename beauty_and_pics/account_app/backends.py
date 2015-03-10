# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
import sys, logging

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger('django.request')

class EmailPasswordAuthBackend(object):
    """Custom authentication backend, log in users users using email and password"""

    def authenticate(self, email=None, password=None):
        """Function to authenticate users via email and password"""
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """Function to get the user instance"""
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
