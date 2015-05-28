# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import Context, Template
from django.conf import settings
from itertools import chain
import calendar, logging, json, sys, re, random

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
    base_url = settings.SITE_URL

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
	'contest_closed',
	'contest_opened',
	'contest_report',
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

    def __init__(self, email_name=None, email_context=None, template_type=None, recipient_list=[], email_type=None, debug_only=False):
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
        if not debug_only:
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
	    return_var += '<div style="text-align: center;font-family: inherit;font-size: 16px;line-height: 32px;color: #ffffff;min-width: 220px">' + str(label) + '</div>'
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

    def contest_report(self):
        """
        Contest report
        Context vars required:
        ->    ['first_name', 'last_name', 'user_email', 'user_id', 'points', ranking]
        """
        
        # debug only
        # self.email_context["ranking"] = 5

        append_random_tip = True
	# common email blocks
	self.email_html_blocks["dear_block"] = self.build_dear_block()
        self.email_html_blocks["main_title_block"] = "ecco il report mensile del concorso."
	# html text email blocks
	self.email_html_blocks["html_main_text_block"] = """
            <table style="width: 100%;">
                <tr>
                    <td>
                        Ti riepiloghiamo le informazioni principali del contest.
                    </td>
                </tr>
                <tr>
                    <td>&nbsp;</td>
                </tr>
                <tr>
                    <td>
                        <b>Punteggio: </b>""" + str(self.email_context.get("points")) + """
                    </td>
                </tr>
                <tr>
                    <td>
                        <b>Posizione: </b>""" + str(self.email_context.get("ranking")) + """
                    </td>
                </tr>
            </table><br />
        """

        if self.email_context.get("ranking") == 1:
            self.email_html_blocks["html_main_text_block"] += "Complimenti, sei in prima posizione, stai andando bene :)<br />"
            append_random_tip = False
        elif self.email_context.get("ranking") <= 10:
            self.email_html_blocks["html_main_text_block"] += "Complimenti, sei tra i primi 10, è il momento di iniziare la scalata verso la pima posizione ;)<br /><br />"

        if append_random_tip:
            # adding random tips
            self.email_html_blocks["html_main_text_block"] += """
                <table style="width: 100%;">
                    <tr>
                        <td>
                            <b>TIP mensile AKA buone regole per ottenere più punti</b>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            """ + self.get_random_tip() + """
                        </td>
                    </tr>
                </table><br />
            """

        self.email_html_blocks["html_main_text_block"] += 'Stanco di ricevere queste email? <a target="_blank" href="' + self.base_url + '/passerella/disiscriviti/' + str(self.email_context.get('user_email')) + '/">Disiscriviti</a>.'

	# plain text email blocks
	self.email_html_blocks["plain_main_text_block"] = """
            Ti riepiloghiamo le informazioni principali del contest. \n
            Punti: """ + str(self.email_context.get("points")) + """\n
            Posizione: """ + str(self.email_context.get("ranking")) + """\n
            Stanco di ricevere queste email? Disiscriviti: """ + self.base_url + '/passerella/disiscriviti/' + str(self.email_context.get('user_email')) + '/' + """
        """

        # call to action blocks
        self.email_html_blocks["html_call_to_action_block"] = self.get_call_to_action_template(href=self.base_url + "/profilo/", label="Accedi al tuo profilo")
        self.email_html_blocks["plain_call_to_action_block"] = "Accedi al tuo profilo: " + self.base_url + "/profilo/"

        # email subject
        self.email_subject = "Beauty & Pics: report mensile del concorso."

        return True

    def contest_opened(self):
        """
        Email on contest opening
        Context vars required:
        ->    ['first_name', 'last_name', 'user_id']
        """

	# common email blocks
	self.email_html_blocks["dear_block"] = self.build_dear_block()
	self.email_html_blocks["main_title_block"] = "Beauty and Pics ha aperto il contest!"
	# html text email blocks
	self.email_html_blocks["html_main_text_block"] = """
            Beauty and Pics ti informa che il contest più atteso dell'anno è APERTO. Ecco
            alcuni consigli su come acquisire punti per scalare la classifica!<br />
            <table style="width: 100%;">
                <tr>
                    <td style="padding-top: 30px;">
                        <b>Condividi la tua pagina profilo sui social networks.</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        Pubblicizzati: più persone visualizzeranno il tuo profilo e maggiori saranno le possibilità di ricevere dei punti.
                    </td>
                </tr>
                <tr>
                    <td style="padding-top: 30px;">
                        <b>Carica un'immagine profilo.</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        Fatti notare: caricando un'immagine profilo che possa attirare l'attenzione, questo invoglierà la gente a cliccare sul tuo profilo!
                    </td>
                </tr>
                <tr>
                    <td style="padding-top: 30px;">
                        <b>Carica le immagini del book.</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        Rendi il tuo profilo interessante caricando le
                        immagini del book. PS: modificando spesso le tue
                        immagini, aumentarai l'interesse della gente a tornare
                        nel tuo profilo, aumentando le probabilità di ricevere
                        dei voti!
                    </td>
                </tr>
            </table><br />
            Questi sono solo alcuni consigli, il resto dipende da te!
        """
	self.email_html_blocks["html_call_to_action_block"] = self.get_call_to_action_template(href=self.base_url + "/passerella/dettaglio-utente/" + str(self.email_context.get("user_id")) + "/", label="Visualizza il mio profilo")
	# plain text email blocks
	self.email_html_blocks["plain_main_text_block"] = "Beauty and Pics ti informa che il contest più atteso dell'anno è APERTO."
	self.email_html_blocks["plain_call_to_action_block"] = "Visualizza il mio profilo: " + self.base_url + "/passerella/dettaglio-utente/" + str(self.email_context.get("user_id")) + "/"

        # email subject
        self.email_subject = "Beauty & Pics: il contest più atteso dell'anno è APERTO."

        return True

    def contest_closed(self):
        """
        Email on contest closing
        Context vars required:
        ->    ['first_name', 'last_name', 'contest_type']
        """

	# common email blocks
	self.email_html_blocks["dear_block"] = self.build_dear_block()
	self.email_html_blocks["main_title_block"] = "Beauty and Pics ha chiuso il contest!"
	# html text email blocks
	self.email_html_blocks["html_main_text_block"] = """
            Beauty and Pics ti informa che il contest è stato <b>CHIUSO</b>.<br /><br />
            Vuoi sapere com'è finita? Accedi subito alla passerella per
            scoprire il vincitore!
        """
	self.email_html_blocks["html_call_to_action_block"] = self.get_call_to_action_template(href=self.base_url + "/passerella/" + str(self.email_context.get("contest_type")) + "/", label="Accedi alla passerella")
	# plain text email blocks
	self.email_html_blocks["plain_main_text_block"] = "Beauty and Pics ti informa che il contest è stato CHIUSO."
	self.email_html_blocks["plain_call_to_action_block"] = "Accedi alla passerella: " + self.base_url + "/passerella/" + str(self.email_context.get("contest_type")) + "/"

        # email subject
        self.email_subject = "Beauty & Pics: contest è stato CHIUSO."

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
	self.email_html_blocks["plain_call_to_action_block"] = "Richiedi aiuto: " + self.base_url + "/richiesta-aiuto"

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
            <table style="width: 100%;">
                <tr>
                    <td>
                        <b>Email:</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        """ + str(self.email_context.get("email")) + """
                    </td>
                </tr>
                <tr>
                    <td>
                        <b>Dettagli della richiesta:</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        """ + str(self.email_context.get("help_text")) + """
                    </td>
                </tr>
            </table>
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
        ->    ['email', 'report_text', 'report_user_id', 'report_user_email', 'report_user_profile_url']
        """

	# common email blocks
	self.email_html_blocks["dear_block"] = "Yo amministratore,"
	self.email_html_blocks["main_title_block"] = "qualcuno ha segnalato un utente."
	# html text email blocks
	self.email_html_blocks["html_main_text_block"] = """
            <table style="width: 100%;">
                <tr>
                    <td>
                        <b>Email (chi ha segnalato):</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        """ + str(self.email_context.get("email")) + """
                    </td>
                </tr>
                <tr>
                    <td>
                        <b>Dettagli della segnalazione (perchè ha segnalato):</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        """ + str(self.email_context.get("report_text")) + """
                    </td>
                </tr>
                <tr>
                    <td>
                        <b>Identificativo dell'utente segnalato:</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        """ + str(self.email_context.get("report_user_id")) + """
                    </td>
                </tr>
                <tr>
                    <td>
                        <b>Email dell'utente segnalato:</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        """ + str(self.email_context.get("report_user_email")) + """
                    </td>
                </tr>
                <tr>
                    <td>
                        <b>Profilo dell'utente segnalato:</b>
                    </td>
                </tr>
                <tr>
                    <td>
                        <a target="_blank" href='""" + str(self.email_context.get("report_user_profile_url")) + """'>""" + str(self.email_context.get("report_user_profile_url")) + """</a>
                    </td>
                </tr>
            </table>
	"""
	self.email_html_blocks["html_call_to_action_block"] = ""
	# plain text email blocks
	self.email_html_blocks["plain_main_text_block"] = """
            * Email (chi ha segnalato) *: """ + str(self.email_context.get("email")) + """ \n
            * Dettagli della segnalazione (perchè ha segnalato) *: """ + str(self.email_context.get("report_text")) + """ \n
            * Identificativo dell'utente segnalato *: """ + str(self.email_context.get("report_user_id")) + """ \n
            * Email dell'utente segnalato *: """ + str(self.email_context.get("report_user_email")) + """ \n
            * Profilo dell'utente segnalato *: """ + str(self.email_context.get("report_user_profile_url")) + """ \n
        """
	self.email_html_blocks["plain_call_to_action_block"] = ""

        # email subject
        self.email_subject = "Beauty & Pics: segnalazione utente."

        return True

    """Functions to create email inner block }}}"""

    def get_random_tip(self):
        """Function to retrieve a random tip"""
        return_var = False
        tips_list = [
            "Condividi spesso la tua pagina profilo sui social networks (Es. Facebook, Twitter, ecc...)",
            "Carica un'immagine profilo che attiri l'attenzione",
            "Aggiungi i tuoi competitori ai preferiti (direttamente dalla loro pagina profilo), per poterli monitorare in tempo reale",
            "Rendi il tuo profilo interessante: carica molte immagini del book e cambiale spesso",
            "Spargi la voce, suggerisci ai tuoi amici e parenti di votarti",
            "Hai dubbi o domande? No problem, scrivici e noi ti risponderemo appena possibile!",
            "Hai dei consigli? Scrivici, siamo sempre felici di ricevere nuove proposte!",
            # adding more priority
            "Condividi spesso la tua pagina profilo sui social networks (Es. Facebook, Twitter, ecc...)",
            "Rendi il tuo profilo interessante: carica molte immagini del book e cambiale spesso",
        ]

        return random.choice(tips_list)

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
	return True
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
