# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import Context, Template
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
        self.template_dir = "email_template/"
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
        """
        Email on recover password form
        Context vars required:
        ->    ['email','password',]
        """

        # email subject
        self.email_subject = "Beauty & Pics: recupero password."
        # email blocks
        self.email_html_blocks["title_block"] = "Titolo della mail"
        self.email_text_blocks["title_block"] = "Titolo della mail"

        main_block_html = """
                <div><b>Email: {{email}}</b></div>
                <div><b>Password: {{password}}</b></div>
        """

        main_block_text = "Email: {{email}} Password: {{password}}"

        # building of email template block
        self.email_html_blocks["main_block"] = self.create_email_block(template=main_block_html, context=self.email_context)
        self.email_text_blocks["main_block"] = self.create_email_block(template=main_block_text, context=self.email_context)

        return True

    def signup_email(self):
        """
        Email on signup form
        Context vars required:
        ->    ['first_name',]
        """

        # email subject
        self.email_subject = "Beauty & Pics ti da il benvenuto."
        # email blocks
        self.email_html_blocks["title_block"] = "Benvenuto al concorso!"
        self.email_text_blocks["title_block"] = "Benvenuto al concorso!"

        main_block_html = """
                <div>Ciao <b>{{first_name}}</b>,</div>
                <div>grazie per esserti registrato in Beauty & Pics!</div>
        """

        main_block_text = "Ciao *{{first_name}}*, grazie per esserti registrato in Beauty & Pics!"

        # building of email template block
        self.email_html_blocks["main_block"] = self.create_email_block(template=main_block_html, context=self.email_context)
        self.email_text_blocks["main_block"] = self.create_email_block(template=main_block_text, context=self.email_context)

        return True

    """Functions to create email inner block }}}"""

    def create_email_block(self, template=None, context=None):
        """Function to build a final email template block. Es. Welcome Joe <- Joe instead of {{name}}"""
        return_var = None

        if template and context:
            t = Template(template)
            c = Context(context)
            return_var = t.render(c)

        return return_var

    def send_mail(self):
        """Function to send email"""

        # build email block
        self.build_email_template()

        # send email
        return_var = send_mail(
            subject=self.email_subject,
            message=self.get_plain_template(),
            from_email=self.email_from,
            recipient_list=self.email_recipient_list,
            html_message=self.get_html_template(),
        )

        logger.debug("email inviate: " + str(return_var) + " destinatari: " + str(self.email_recipient_list))
        return return_var
