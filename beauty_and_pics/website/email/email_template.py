# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.template.loader import render_to_string
import calendar, logging, json, sys, re

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class CustomEmailTemplate():

    def __init__(self):
        self.template_name = None # set the template name
        self.template_dir = "website/email_template/"
        self.email_context = {}
        self.email_subject = ""
        self.email_from = "no-reply@entpy.com"
        self.email_recipient_list = ['developer@entpy.com',]

    def get_html_template(self):
        """Function to create html template"""

        return_var = False
        if self.template_name:
            return_var = render_to_string(self.template_dir + self.template_name + '.html', self.email_context)
        return return_var

    def get_plain_template(self):
        """Function to create plain text template"""

        return_var = False
        if self.template_name:
            return_var = render_to_string(self.template_dir + self.template_name + '.txt', self.email_context)
        return return_var

    def send_mail(self):
        """Function to send email"""
        return_var = send_mail(
            subject=self.email_subject,
            message=self.get_plain_template(),
            from_email=self.email_from,
            recipient_list=self.email_recipient_list,
            html_message=self.get_html_template(),
        )

        logger.debug("email inviate: " + str(return_var) + " destinatari: " + str(self.email_recipient_list))
        return return_var
