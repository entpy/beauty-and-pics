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

    # the email name, es recover_password_email
    email_name = None

    # the email data, es email and password in recover password email
    email_context = {}

    # the email inner block (html and text only)
    email_html_blocks = {"main_block": ""}
    email_text_blocks = {"main_block": ""}

    # email subject
    email_subject = None

    # email template name
    template_name = "default_template"

    # available email name
    available_email_name = (
                            'recover_password_email',
                           )

    def __init__(self, email_name=None, email_context=None):
        self.template_dir = "website/email_template/"
        self.email_from = "no-reply@entpy.com"
        self.email_recipient_list = ['developer@entpy.com',]

        # setting email name and context
        self.email_name = email_name
        self.email_context = email_context

        # building template

    def get_html_template(self):
        """Function to create html template"""

        return_var = False
        if self.template_name:
            return_var = render_to_string(self.template_dir + self.template_name + '.html', self.email_html_blocks)
        return return_var

    def get_plain_template(self):
        """Function to create plain text template"""

        return_var = False
        if self.template_name:
            return_var = render_to_string(self.template_dir + self.template_name + '.txt', self.email_text_blocks)
        return return_var

    def build_email_template(self):
        """Function to create the email template before sending"""

        return_var = False
        if self.email_name in self.available_email_name:
            exec("self." + self.email_name + "()")
            return_var = True
        else:
            logger.error("mail name " + str(self.email_name) + " is not a valid email template")

        return return_var

    """Functions to create email inner block {{{"""

    def recover_password_email(self):
        """Function to populate email_html_blocks, email_text_blocks, email_subject and template_name"""

        self.email_html_blocks = self.email_html_blocks["title_block"] = "Titolo della mail"
        self.email_text_blocks = self.email_text_blocks["title_block"] = "Titolo della mail"
        self.email_subject = "Beauty & Pics: recupero password."

        main_block_html = """
                <div><b>Email: {email}</b></div>
                <div><b>Password: {password}</b></div>
        """

        main_block_text = "Email: {email} Password: {password}"

        # TODO: build "main_blocks" starting from "email_context"
        # sostiutire nei blocchi html e text le variabili per ottenere i
        # blocchi interni del template

        self.email_html_blocks = self.email_html_blocks["main_block"] = """
                <div><b>Email: " + str(self.email_context["email"]) + "</b></div>\
                <div><b>Password: " + str(self.email_context["password"]) + "</b></div>\
        """
        self.email_text_blocks = self.email_text_blocks["main_block"] = """
                "email: " + str(self.email_context["email"]) + " password: " + str("self.email_context["password"]")
        """

        return True

    """Functions to create email inner block }}}"""

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
