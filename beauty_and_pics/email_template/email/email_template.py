# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import Context, Template
from itertools import chain
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

    # base url
    base_url = "http://127.0.0.1:8000"

    # the email inner blocks
    email_html_blocks = { "base_url": base_url, }

    # email subject
    email_subject = None

    # email template name
    template_name = None

    # available email name
    available_email_name = (
	'recover_password_email',
	'signup_email',
	'help_request_email',
	'report_user_email',
   )

    # email template directory
    template_dir = "email_template/"

    # list of email template available
    template_type = {
	"default": "default_template",
	"user": "user_template",
	"admin": "admin_template",
    }

    email_ready_to_send = False

    def __init__(self, email_name=None, email_context=None, template_type=None, recipient_list=[], email_type=None):
        self.email_from = "no-reply@entpy.com"

        # load recipient list
        self.email_recipient_list = recipient_list
	if email_type == "admin_email":
	    self.email_recipient_list = ['developer@entpy.com',]
	else:
	    # TODO: plz remove, only for debug
	    self.email_recipient_list += ['developer@entpy.com',] 

        # setting email name and context
        self.email_name = email_name
        self.email_context = email_context

        # setting template name, this override default template name
        self.set_template_name(template_type=template_type)

        # build email block
        self.build_email_template()

        # send email
        self.send_mail()

    def build_dear_block(self):
	"""Function to build dear block"""
	return_var = False
	first_name = self.email_context.get("first_name")
	last_name = self.email_context.get("last_name")
	if last_name:
	    last_name = " " + last_name

	if first_name:
	    return_var = "Caro/a " + str(first_name)+str(last_name)+","

	return return_var

    def get_call_to_action_template(self, href=None, label=None):
	"""Function to retrieve call to action template"""
	return_var = False

	if href and label:
	    return_var = '<a style="display: inline-block;text-decoration: none;-webkit-text-size-adjust: none;mso-hide: all;text-align: center;font-family: Verdana,Geneva,sans-serif;-webkit-border-radius: 4px;-moz-border-radius: 4px;border-radius: 4px;border-top: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-left: 0px solid transparent;color: #ffffff !important;padding: 5px 20px 5px 20px;vertical-align: middle" href="' + str(href) + '" target="_blank">'
	    return_var += '<!--[if gte mso 9]>&nbsp;<![endif]-->'
	    return_var += '<div style="text-align: center;font-family: inherit;font-size: 16px;line-height: 32px;color: #ffffff;min-width: 140px">' + str(label) + '</div>'
	    return_var += '<!--[if gte mso 9]>&nbsp;<![endif]-->'
	    return_var += '</a>'

	return return_var

    def set_template_name(self, template_type=None):
        """Function to set a template name starting from template type"""
        self.template_name = self.template_type.get(template_type, "default")

        return True

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
            return_var = render_to_string(self.template_dir + self.template_name + '.txt', self.email_html_blocks)

        return return_var

    def build_email_template(self):
        """Function to create the email template before sending"""
        return_var = False
	if self.email_name in chain(self.available_email_name):
            exec("self." + self.email_name + "()")
            return_var = True
	    self.email_ready_to_send = True
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

	# common email blocks
	self.email_html_blocks["dear_block"] = self.build_dear_block()
	self.email_html_blocks["main_title_block"] = "ecco le tua nuova password."
	# html text email blocks
	self.email_html_blocks["html_main_text_block"] = """
	    Abbiamo generato una nuova password...non la perdere!<br />
	    Puoi accedere con le seguenti credenziali:<br />
	    <ul>
		<li><b>Email:</b> """ + str(self.email_context.get("email")) + """</li>
		<li><b>Password:</b> """ + str(self.email_context.get("password")) + """</li>
	    </ul><br />
	    Per motivi di sicurezza, modifica la tua password appena possibile nella tua area privata.
	"""
	self.email_html_blocks["html_call_to_action_block"] = self.get_call_to_action_template(href=self.base_url + "/profilo/zona-proibita/", label="Accedi ora")
	# plain text email blocks
	self.email_html_blocks["plain_main_text_block"] = "Puoi accedere con le seguenti credenziali \nEmail: " + str(self.email_context.get("email")) + " \nPassword: " + str(self.email_context.get("password")) + " \nPer motivi di sicurezza, modifica la tua password appena possibile nella tua area privata."
	self.email_html_blocks["plain_call_to_action_block"] = "Accedi ora: " + self.base_url + "/profilo/zona-proibita/"

        # email subject
        self.email_subject = "Beauty & Pics: recupero password."

        return True

    def signup_email(self):
        """
        Email on signup form
        Context vars required:
        ->    ['first_name', 'last_name',]
        """

	# common email blocks
	self.email_html_blocks["dear_block"] = self.build_dear_block()
	self.email_html_blocks["main_title_block"] = "Beauty and Pics ti da il benvenuto!"
	# html text email blocks
	self.email_html_blocks["html_main_text_block"] = "Grazie per esserti registrato"
	self.email_html_blocks["html_call_to_action_block"] = self.get_call_to_action_template(href=self.base_url + "/richiesta-aiuto", label="Chiedi aiuto")
	# plain text email blocks
	self.email_html_blocks["plain_main_text_block"] = "Grazie per esserti registrato"
	self.email_html_blocks["plain_call_to_action_block"] = "Richiedi aiuto:" + self.base_url + "/richiesta-aiuto"

        # email subject
        self.email_subject = "Beauty & Pics ti da il benvenuto."

        return True

    def help_request_email(self):
        """
        Email on help form
        Context vars required:
        ->    ['email', 'help_text',]
        """

	# common email blocks
	self.email_html_blocks["dear_block"] = "Yo amministratore,"
	self.email_html_blocks["main_title_block"] = "qualcuno chiede aiuto."
	# html text email blocks
	self.email_html_blocks["html_main_text_block"] = """
	    <div><b>Email:</b></div>
	    <div>""" + str(self.email_context.get("email")) + """</div><br />
	    <div><b>Dettagli della richiesta:</b></div>
	    <div>""" + str(self.email_context.get("help_text")) + """</div>
	"""
	self.email_html_blocks["html_call_to_action_block"] = ""
	# plain text email blocks
	self.email_html_blocks["plain_main_text_block"] = "* Email *: " + str(self.email_context.get("email")) + " \n* Richiesta *: " + str(self.email_context.get("help_text"))
	self.email_html_blocks["plain_call_to_action_block"] = ""

        # email subject
        self.email_subject = "Beauty & Pics: richiesta di aiuto."

        return True

    def report_user_email(self):
        """
        Email on help form
        Context vars required:
        ->    ['email', 'report_text',]
        """

	# common email blocks
	self.email_html_blocks["dear_block"] = "Yo amministratore,"
	self.email_html_blocks["main_title_block"] = "qualcuno ha segnalato un utente."
	# html text email blocks
	self.email_html_blocks["html_main_text_block"] = """
	    <div><b>Email (chi ha segnalato):</b></div>
	    <div>""" + str(self.email_context.get("email")) + """</div><br />
	    <div><b>Dettagli della segnalazione (perchè ha segnalato):</b></div>
	    <div>""" + str(self.email_context.get("report_text")) + """</div>
	"""
	self.email_html_blocks["html_call_to_action_block"] = ""
	# plain text email blocks
	self.email_html_blocks["plain_main_text_block"] = "* Email (chi ha segnalato) *: " + str(self.email_context.get("email")) + " \n* Dettagli della segnalazione (perchè ha segnalato) *: " + str(self.email_context.get("report_text"))
	self.email_html_blocks["plain_call_to_action_block"] = ""

        # email subject
        self.email_subject = "Beauty & Pics: segnalazione utente."

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
	return_var = False
        # send email
	if self.email_ready_to_send:
	    return_var = send_mail(
		subject=self.email_subject,
		message=self.get_plain_template(),
		from_email=self.email_from,
		recipient_list=self.email_recipient_list,
		html_message=self.get_html_template(),
	    )
	    logger.debug("email inviate: " + str(return_var) + " destinatari: " + str(self.email_recipient_list))

        return return_var
