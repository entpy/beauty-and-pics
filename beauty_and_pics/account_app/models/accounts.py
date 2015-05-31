# -*- coding: utf-8 -*-

from django.db import models
from django.db import connection
from datetime import date
from dateutil.relativedelta import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from contest_app.models.contest_types import Contest_Type
from contest_app.models.points import Point
from account_app.models.images import Book
from email_template.email.email_template import *
from website.exceptions import *
from beauty_and_pics.consts import project_constants
from django.db.models import Q, F, Count, Sum
import sys, logging, base64, hashlib, string, random

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

# extends User model
class Account(models.Model):
    # id_account = models.AutoField(primary_key=True)
    # Links Account to a User model instance.
    user = models.OneToOneField(User, primary_key=True)
    contest_type = models.ForeignKey(Contest_Type, null=True)
    city = models.CharField(max_length=100, null=True)
    # TODO: https://github.com/coderholic/django-cities
    country = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    status = models.IntegerField(null=True)
    birthday_date = models.DateField(null=True)
    hair = models.CharField(max_length=15, null=True) 
    eyes = models.CharField(max_length=15, null=True)
    height = models.CharField(max_length=4, null=True)
    newsletters_bitmask = models.CharField(max_length=20, default=(project_constants.WEEKLY_REPORT_EMAIL_BITMASK + project_constants.CONTEST_REPORT_EMAIL_BITMASK), null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'account_app'

    def __unicode__(self):
        return self.user.username

    # bitwise functions {{{
    def check_bitmask(self, b1, b2):
        """Function to compare two bitmask 'b1' and 'b2'"""
        return int(b1) & int(b2)

    def add_bitmask(self, bitmask, add_value):
        """Function to add bitmask 'add_value' to 'bitmask'"""
        return int(bitmask) | int(add_value);

    def remove_bitmask(self, bitmask, remove_value):
        """Function to remove bitmask 'remove_value' from 'bitmask'"""
        return int(bitmask) & (~int(remove_value));
    # bitwise functions }}}

    def check_if_email_exists(self, email_to_check=None):
        """Function to check if an email already exists"""
        return_var = None
        try:
            User.objects.get(email=email_to_check)
            return_var = True
        except User.DoesNotExist:
            return_var = False

	return return_var

    def get_user_about_email(self, email=None):
        """Function to retrieve user about an email"""
        return_var = None
        try:
            return_var = User.objects.get(email=email)
        except User.DoesNotExist:
            raise

        return return_var

    def get_user_about_id(self, user_id=None):
        """Function to retrieve user about id"""
        return_var = None
        try:
            return_var = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise

        return return_var

    def delete_user(self, user_id=None, logged_user_id=None):
        """Function to delete user"""
        if user_id and logged_user_id:
            if user_id == logged_user_id:
                try:
                    user_obj = User.objects.get(pk=user_id)
                    user_obj.delete()
                except User.DoesNotExist:
                    raise UserDeleteDoesNotExistsError
            else:
                raise UserDeleteIdDoesNotMatchError
        else:
            raise UserDeleteDoesNotExistsError

        return True

    def register_account(self, user_info=None):
        """Function to register a new account"""

        return_var = False
        if user_info:
            account_obj = Account()
            # create new account
            new_user = account_obj.create_user_account(email=user_info["email"], password=user_info["password"])

            # identify contest type
            contest_type_obj = Contest_Type()
            if user_info["gender"] == project_constants.WOMAN_GENDER:
                user_info["contest_type"] = contest_type_obj.get_contest_type_by_code(code=project_constants.WOMAN_CONTEST)
            elif user_info["gender"] == project_constants.MAN_GENDER:
                user_info["contest_type"] = contest_type_obj.get_contest_type_by_code(code=project_constants.MAN_CONTEST)

	    logger.debug("tipo di contest rilevato: '" + str(user_info["contest_type"]) + "'")

            # insert addictional data inside User and Account models
            account_obj.update_data(save_data=user_info, user_obj=new_user)
            return_var = True

        return return_var

    def create_user_account(self, email=None, password=None):
        """Function to create user and related account"""
        return_var = False
        account_obj = Account()
        if email and password:
            if not self.check_if_email_exists(email_to_check=email):
                account_obj.user = User.objects.create_user(username=self.__email_to_username(email), email=email, password=password)
                # add "catwalk_user" group in user groups
                account_obj.user.groups.add(self.__create_defaul_user_group())
                account_obj.save()
                return_var = account_obj.user

                # raise an exception if occur errors in account creation
                if not return_var:
                    raise UserCreateError

        return return_var

    def __create_defaul_user_group(self):
        """Function to [create if not exists and] retrieve catwalk_user group"""
        return_var = None
        try:
            return_var = Group.objects.get(name=project_constants.CATWALK_GROUP_NAME)
        except Group.DoesNotExist:
            # group must be created
            group = Group(name=project_constants.CATWALK_GROUP_NAME)
            group.save()
            return_var = group

        return return_var

    def __email_to_username(self, email):
        """
        Function to convert email to username
        taken from -> https://github.com/dabapps/django-email-as-username/blob/master/emailusernames/utils.py
        """
        # Emails should be case-insensitive unique
        email = email.lower()
        # Deal with internationalized email addresses
        converted = email.encode('utf8', 'ignore')
        return base64.urlsafe_b64encode(hashlib.sha256(converted).digest())[:30]

    # TODO: try to manual raise error in this function
    def update_email_password(self, current_email=None, new_email=None, password=None):
        """Function to update email and password about a user"""
        return_var = False
        if current_email:
            try:
                user_obj = User.objects.get(email=current_email)
            except User.DoesNotExist:
                # send exception to parent try-except block
                raise
            else:
                # save new password
                if password:
                    user_obj.set_password(password)
                # save new email
                if new_email:
                    user_obj.email = new_email
                    # create new username starting from email
                    user_obj.username = self.__email_to_username(email=new_email)
                # save account instance
                if password or new_email:
                    user_obj.save()
                return_var = True

        if not return_var:
            raise UserEmailPasswordUpdateError

        return return_var

    def update_data(self, save_data=None, user_obj=None):
        """Function to save data inside db"""
        return_var = False

        if save_data and user_obj:
            # save User model addictional informations
            if "first_name" in save_data:
                user_obj.first_name = save_data["first_name"]
            if "last_name" in save_data:
                user_obj.last_name = save_data["last_name"]
            # save Account model addictional informations
            if "city" in save_data:
                user_obj.account.city = save_data["city"]
            if "country" in save_data:
                user_obj.account.country = save_data["country"]
            if "gender" in save_data:
                user_obj.account.gender = save_data["gender"]
            if "contest_type" in save_data:
                user_obj.account.contest_type = save_data["contest_type"]
            if "status" in save_data:
                user_obj.account.status = save_data["status"]
            if "birthday_date" in save_data:
                user_obj.account.birthday_date = save_data["birthday_date"]
            if "hair" in save_data:
                user_obj.account.hair = save_data["hair"]
            if "eyes" in save_data:
                user_obj.account.eyes = save_data["eyes"]
            if "height" in save_data:
                user_obj.account.height = save_data["height"]
            # save addictiona models data
            user_obj.save()
            user_obj.account.save()
            return_var = user_obj

        if not return_var:
            raise UserUpdateDataError

	return return_var

    def create_date(self, date_dictionary=None, get_isoformat=False):
        """Function to create birthday date starting from dd, mm, yyyy"""
        return_var = False

        if date_dictionary:
            day = date_dictionary.get("day")
            month = date_dictionary.get("month")
            year = date_dictionary.get("year")

            # building birthday date
            if (day and month and year):
                if get_isoformat:
                    return_var = date(year=int(year), month=int(month), day=int(day)).isoformat()
                else:
                    return_var = date(year=int(year), month=int(month), day=int(day))

        return return_var

    def create_login_session(self, email=None, password=None, request=None):
        """Function to create a login session (logging user inside website)"""
        return_var = False

        if (email and password and request):
            # Use custom email-password backend to check if the email/password
            # combination is valid - a User object is returned if it is.
            user_obj = authenticate(email=email, password=password)

            # If we have a User object, the email and password are correct.
            # If None (Python's way of representing the absence of a value), no user
            # with matching credentials was found.
            if user_obj:
                # Is the account active? It could have been disabled.
                if user_obj.is_active:
                    # If the account is valid and active, we can log the user in.
                    login(request, user_obj)
                    return_var = True
                else:
                    # An inactive account was used - no logging in!
                    raise UserNotActiveError
            else:
                # Ops...email or password not valid - no logging in!
                raise UserLoginError

        return return_var

    def generate_new_password(self):
        """Function to generate a new password"""
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    def check_user_password(self, request=None, password_to_check=None):
        """Function to check if a password match the current logged in user password"""
        return_var = False
        if request and password_to_check:
            # to see how it works see the docs
            if not request.user.check_password(password_to_check):
                raise UserPasswordMatchError
            return_var = True

        return return_var

    def get_autenticated_user_email(self, request=None):
        """Function to retrieve the email address about current logged in user"""
        return_var = False
        if request and request.user.is_authenticated():
            return_var = request.user.email
            logger.info("email of current logged in user: " + str(return_var))

        return return_var

    def get_autenticated_user_data(self, request=None):
        """
        Function to retrieve current user/account logged in data (es. first_name, last_name, gender, ecc...)
        """
        return_var = {}

        if request and request.user.is_authenticated():
            return_var = self.get_user_data_as_dictionary(user_obj=request.user)
            # logger.info("data about current logged in user: " + str(return_var))

        return return_var

    def custom_user_id_data(self, user_id=None):
        """Function to retrieve user/account info about user id"""
        return_var = {}

        if user_id:
	    try:
	        user_obj = self.get_user_about_id(user_id=user_id)
            except User.DoesNotExist:
	        raise
            else:
                return_var = self.get_user_data_as_dictionary(user_obj=user_obj)

        return return_var

    def get_user_data_as_dictionary(self, user_obj=None):
        """Function to convert a user object into dictionary"""
        return_var = {}
        if user_obj:
            # from user model {{{
            return_var["user_id"] = user_obj.id or ''
            return_var["first_name"] = user_obj.first_name or ''
            return_var["last_name"] = user_obj.last_name or ''
            return_var["email"] = user_obj.email or ''
            # from user model }}}
            # from account model {{{
	    try:
		return_var["city"] = user_obj.account.city or ''
		return_var["country"] = user_obj.account.country or ''
		return_var["gender"] = user_obj.account.gender or ''
		return_var["contest_type"] = user_obj.account.contest_type or ''
		return_var["birthday_date"] = user_obj.account.birthday_date or ''
		return_var["birthday_day"] = str(user_obj.account.birthday_date.day) or ''
		return_var["birthday_month"] = str(user_obj.account.birthday_date.month) or ''
		return_var["birthday_year"] = str(user_obj.account.birthday_date.year) or ''
		return_var["age"] = str(relativedelta(date.today(), user_obj.account.birthday_date).years) or ''
		return_var["hair"] = user_obj.account.hair or ''
		return_var["eyes"] = user_obj.account.eyes or ''
		return_var["height"] = user_obj.account.height or ''
	    except Account.DoesNotExist:
		pass
            # from account model }}}

        return return_var

    def get_contest_account_info(self, user_id=None, contest_type=None):
        """
            Function to retrieve contest account info:
            ranking
            total points
            percentage global metric
            percentage smile metric
            percentage look metric
        """

        point_obj = Point()
        contest_account_info = {}
        contest_account_info["total_points"] = 0

        # retrieve account contest info
        user_metric_points = point_obj.get_single_user_contest_info(user_id=user_id)

        if user_metric_points:
            for single_metric in user_metric_points:
                contest_account_info[single_metric["metric__name"]] = {}
                contest_account_info[single_metric["metric__name"]]["total_points"] = single_metric["total_points"]
                contest_account_info[single_metric["metric__name"]]["total_votes"] = single_metric["total_votes"]
                contest_account_info[single_metric["metric__name"]]["metric_rate_percentage"] = int((single_metric["total_points"] / (single_metric["total_votes"] * 5.0)) * 100)
                contest_account_info["total_points"] += single_metric["total_points"]

        # retrieve user ranking
        contest_account_info["ranking"] = self.get_user_contest_ranking(user_id=user_id, contest_type=contest_type)

        logger.debug("contest account info retrieved: " + str(contest_account_info))

        # totale punti per ogni utente -> QUESTA FUNZIONE NON VA QUI
        """
        total_points = Point.objects.values('user__id').filter(contest__contest_type=F('user__account__contest_type'),
                contest__status=project_constants.CONTEST_ACTIVE).annotate(totale=Sum('points'))
        """

        return contest_account_info

    def get_top_five_contest_user(self, contest_type=None, hall_of_fame=False):
        """Function to retrieve the top five contest user"""
        user = None
        book_obj = Book()
        top_five_account = []
        filters_list = {"filter_name": "classification", "start_limit": "0", "show_limit": "5"}
        filtered_elements = self.get_filtered_accounts_list(filters_list=filters_list, contest_type=contest_type)
        for user_info in filtered_elements:
            # logger.debug("element list: " + str(user_info))
            # retrieve extra params in hall of fame case
            if hall_of_fame:
                try:
		    user = self.get_user_about_id(user_id=user_info["user__id"])
		except User.DoesNotExist:
                    user = {}
		    pass

            top_five_account.append({
                "user_id": user_info["user__id"],
                "user": user,
                "user_first_name": user_info["user__first_name"],
                "user_last_name": user_info["user__last_name"],
                "user_email": user_info.get("user__email"),
                "user_profile_thumbnail_image_url": book_obj.get_profile_thumbnail_image_url(user_id=user_info["user__id"]),
                "user_profile_image_url": book_obj.get_profile_image_url(user_id=user_info["user__id"]),
                "user_total_points": user_info.get("total_points"),
            }),

        return top_five_account

    def get_filtered_accounts_list(self, contest_type, filters_list=None):
        """Function to retrieve a list of filtere accounts"""
        return_var = False
        # logger.debug("NOME FILTRO: " + str(filters_list["filter_name"]))

        # filter only catwalker users

        # order by "latest_registered" filter
        if filters_list["filter_name"] == "latest_registered":
            return_var = Account.objects.values('user__first_name', 'user__last_name', 'user__email', 'user__id', 'user__account__newsletters_bitmask').filter(user__groups__name=project_constants.CATWALK_GROUP_NAME, contest_type__code=contest_type)
            return_var = return_var.order_by('-user__account__creation_date')

        # order by "classification" filter
        if filters_list["filter_name"] == "classification":
            # "contest__status" to identify point about current contest
            # più leggera ma non mostra gli utenti che non hanno ancora punti
            return_var = Point.objects.values('user__first_name', 'user__last_name', 'user__email', 'user__id', 'user__account__newsletters_bitmask').filter(user__groups__name=project_constants.CATWALK_GROUP_NAME, contest__status=project_constants.CONTEST_ACTIVE, contest__contest_type__code=contest_type).annotate(total_points=Sum('points'))
            # più pesante e mostra anche gli utenti che non hanno ancora punti
            # return_var = Account.objects.values('user__first_name', 'user__last_name', 'user__email', 'user__id').filter(user__groups__name=project_constants.CATWALK_GROUP_NAME, contest_type__contest__status=project_constants.CONTEST_ACTIVE).annotate(total_points=Sum('user__point__points'))
            return_var = return_var.order_by('-total_points', 'user__id')

        # order by "most_beautiful_smile" filter
        if filters_list["filter_name"] == "most_beautiful_smile":
            # "contest__status" to identify point about current contest
            # più leggera ma non mostra gli utenti che non hanno ancora punti
            return_var = Point.objects.values('user__first_name', 'user__last_name', 'user__email', 'user__id', 'user__account__newsletters_bitmask').filter(user__groups__name=project_constants.CATWALK_GROUP_NAME, contest__status=project_constants.CONTEST_ACTIVE, contest__contest_type__code=contest_type, metric__name=project_constants.VOTE_METRICS_LIST["smile_metric"]).annotate(total_points=Sum('points'))
            # più pesante e mostra anche gli utenti che non hanno ancora punti
            # return_var = Account.objects.values('user__first_name', 'user__last_name', 'user__email', 'user__id').filter(Q(user__point__metric__name=project_constants.VOTE_METRICS_LIST["smile_metric"]) | Q(user__point__isnull=True), user__groups__name=project_constants.CATWALK_GROUP_NAME, contest_type__contest__status=project_constants.CONTEST_ACTIVE).annotate(total_points=Sum('user__point__points'))
            return_var = return_var.order_by('-total_points', 'user__id')

        # order by "look_more_beautiful" filter
        if filters_list["filter_name"] == "look_more_beautiful":
            # "contest__status" to identify point about current contest
            # più leggera ma non mostra gli utenti che non hanno ancora punti
            return_var = Point.objects.values('user__first_name',
                    'user__last_name', 'user__email', 'user__id', 'user__account__newsletters_bitmask').filter(user__groups__name=project_constants.CATWALK_GROUP_NAME, contest__status=project_constants.CONTEST_ACTIVE, contest__contest_type__code=contest_type, metric__name=project_constants.VOTE_METRICS_LIST["look_metric"]).annotate(total_points=Sum('points'))
            # più pesante e mostra anche gli utenti che non hanno ancora punti
            # return_var = Account.objects.values('user__first_name', 'user__last_name', 'user__email', 'user__id').filter(user__groups__name=project_constants.CATWALK_GROUP_NAME, contest_type__contest__status=project_constants.CONTEST_ACTIVE).filter(Q(user__point__metric__name=project_constants.VOTE_METRICS_LIST["look_metric"]) | Q(user__point__metric__isnull=True)).annotate(total_points=Sum('user__point__points'))
            return_var = return_var.order_by('-total_points', 'user__id')

        # limits filter
        #logger.debug("limite da: " + str(filters_list["start_limit"]))
        #logger.debug("limite numero elementi: " + str(filters_list["show_limit"]))
        if filters_list.get("start_limit") and filters_list.get("show_limit"):
            return_var = return_var[filters_list["start_limit"]:filters_list["show_limit"]]

        #logger.debug("@@@: " + str(return_var))

        return return_var

    def get_user_contest_ranking(self, user_id=None, contest_type=None):
        """Function to retrieve current user contest ranking"""
        cursor = connection.cursor()
        # il db è come la dieta, va variato spesso
        # questo potrebbe non piacere a molti -> http://stackoverflow.com/questions/18846174/django-detect-database-backend
        if connection.vendor == "postgresql":
            # PostgreSQL query
            cursor.execute('SELECT "ranking_table"."ranking", "user_id" FROM( SELECT row_number() OVER (ORDER BY SUM("contest_app_point"."points") DESC) as "ranking", "contest_app_point"."user_id", SUM("contest_app_point"."points") AS "total_points" FROM "contest_app_point" INNER JOIN "auth_user" ON ( "contest_app_point"."user_id" = "auth_user"."id" ) INNER JOIN "auth_user_groups" ON ( "auth_user"."id" = "auth_user_groups"."user_id" ) INNER JOIN "auth_group" ON ( "auth_user_groups"."group_id" = "auth_group"."id" ) INNER JOIN "contest_app_contest" ON ( "contest_app_point"."contest_id" = "contest_app_contest"."id_contest" ) INNER JOIN "contest_app_contest_type" ON ( "contest_app_contest"."contest_type_id" = "contest_app_contest_type"."id_contest_type" ) WHERE "auth_group"."name" = \'catwalk_user\' AND "contest_app_contest_type"."code" = %(contest_type)s AND "contest_app_contest"."status" = \'active\' GROUP BY "contest_app_point"."user_id" ORDER BY "total_points" DESC, "contest_app_point"."user_id" ASC) AS "ranking_table" WHERE "user_id" = %(user_id)s', {"user_id": user_id, "contest_type": contest_type})
        else:
            # MySQL query
            cursor.execute("SET @row_number:=0;")
            # cursor.execute("SELECT `ranking_table`.`ranking` FROM (SELECT @row_number:=@row_number+1 AS `ranking`, `contest_app_point`.`user_id`, SUM(`contest_app_point`.`points`) AS `total_points` FROM `contest_app_point` INNER JOIN `auth_user` ON ( `contest_app_point`.`user_id` = `auth_user`.`id` ) INNER JOIN `auth_user_groups` ON ( `auth_user`.`id` = `auth_user_groups`.`user_id` ) INNER JOIN `auth_group` ON ( `auth_user_groups`.`group_id` = `auth_group`.`id` ) INNER JOIN `contest_app_contest` ON ( `contest_app_point`.`contest_id` = `contest_app_contest`.`id_contest` ) WHERE (`auth_group`.`name` = 'catwalk_user' AND `contest_app_contest`.`status` = 'active') GROUP BY `contest_app_point`.`user_id` ORDER BY `total_points` DESC, `contest_app_point`.`user_id` ASC) AS `ranking_table` WHERE `user_id` = %s", [user_id])
            cursor.execute("SELECT `ranking` FROM (SELECT @row_number:=@row_number+1 AS `ranking`, `user_id`, `total_points` FROM (SELECT `contest_app_point`.`user_id`, SUM(`contest_app_point`.`points`) AS `total_points` FROM `contest_app_point` INNER JOIN `auth_user` ON ( `contest_app_point`.`user_id` = `auth_user`.`id` ) INNER JOIN `auth_user_groups` ON ( `auth_user`.`id` = `auth_user_groups`.`user_id` ) INNER JOIN `auth_group` ON ( `auth_user_groups`.`group_id` = `auth_group`.`id` ) INNER JOIN `contest_app_contest` ON ( `contest_app_point`.`contest_id` = `contest_app_contest`.`id_contest` ) INNER JOIN `contest_app_contest_type` ON ( `contest_app_contest`.`contest_type_id` = `contest_app_contest_type`.`id_contest_type` ) WHERE (`auth_group`.`name` = 'catwalk_user' AND `contest_app_contest_type`.`code` = %(contest_type)s AND `contest_app_contest`.`status` = 'active') GROUP BY `contest_app_point`.`user_id` ORDER BY `total_points` DESC, `contest_app_point`.`user_id` ASC) AS `ranking_table`) AS `user_ranking` WHERE `user_id` = %(user_id)s", {"user_id": user_id, "contest_type": contest_type})

        row = cursor.fetchall()
        return_var = row[0][0] if row else None

        return return_var

    def send_contest_opening_emails(self, contest_type):
        """Function to send email filters_list["filter_name"] == "latest_registered"on contest opening"""
        filters_list = {}
        filters_list["filter_name"] = "latest_registered"
        account_list = self.get_filtered_accounts_list(filters_list=filters_list, contest_type=contest_type)
        if account_list:
            for single_account in account_list:
                if not self.check_bitmask(b1=single_account["user__account__newsletters_bitmask"], b2=project_constants.CONTEST_REPORT_EMAIL_BITMASK):
                    # skip loop if the user doesn't want to receive this notify
                    continue
                logger.debug("contest_opened EMAIL DA INVIARE: " + str(single_account["user__email"]))
		# contest opening email
		email_context = {
		    "first_name": single_account["user__first_name"],
		    "last_name": single_account["user__last_name"],
		    "user_id": single_account["user__id"],
                }
		CustomEmailTemplate(
		    email_name="contest_opened",
		    email_context=email_context,
		    template_type="user",
		    recipient_list=[single_account["user__email"],]
		)

        return True

    def send_contest_closing_emails(self, contest_type):
        """Function to send email on contest closing"""
        filters_list = {}
        filters_list["filter_name"] = "latest_registered"
        account_list = self.get_filtered_accounts_list(filters_list=filters_list, contest_type=contest_type)
        if account_list:
            for single_account in account_list:
                if not self.check_bitmask(b1=single_account["user__account__newsletters_bitmask"], b2=project_constants.CONTEST_REPORT_EMAIL_BITMASK):
                    # skip loop if the user doesn't want to receive this notify
                    continue
                logger.debug("contest_closed EMAIL DA INVIARE: " + str(single_account["user__email"]))
		# contest opening email
		email_context = {
		    "first_name": single_account["user__first_name"],
		    "last_name": single_account["user__last_name"],
		    "contest_type": contest_type,
                }
		CustomEmailTemplate(
		    email_name="contest_closed",
		    email_context=email_context,
		    template_type="user",
		    recipient_list=[single_account["user__email"],]
		)

        return True

    def send_report_emails(self, contest_type):
        """
            Function to send report email
            ['first_name', 'last_name', 'user_email', 'user_id', 'points', ranking]
            Agli utenti che non hanno voti non invio la mail (risultato con il
            filtro 'classification', dove tiro fuori gli utenti se hanno dei
            punti)
        """

        filters_list = {}
        filters_list["filter_name"] = "classification"
        account_list = self.get_filtered_accounts_list(filters_list=filters_list, contest_type=contest_type)
        if account_list:
            for single_account in account_list:
                if not self.check_bitmask(b1=single_account["user__account__newsletters_bitmask"], b2=project_constants.WEEKLY_REPORT_EMAIL_BITMASK):
                    # skip loop if the user doesn't want to receive this notify
                    continue
                logger.debug("contest_report EMAIL DA INVIARE: " + str(single_account["user__email"]))
                account_info = self.get_contest_account_info(user_id=single_account["user__id"], contest_type=contest_type)
		# contest opening email
		email_context = {
		    "first_name": single_account["user__first_name"],
		    "last_name": single_account["user__last_name"],
		    "user_email": single_account["user__email"],
		    "user_id": single_account["user__id"],
		    "points": account_info["total_points"],
		    "ranking": account_info["ranking"],
                }
		CustomEmailTemplate(
		    email_name="contest_report",
		    email_context=email_context,
		    template_type="user",
		    recipient_list=[single_account["user__email"],]
		)

        return True
