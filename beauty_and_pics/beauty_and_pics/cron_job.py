# -*- coding: utf-8 -*-

from django_cron import CronJobBase, Schedule
from django.conf import settings
from contest_app.models.contests import *
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ContestManagerJob(CronJobBase):
    """Cron to manage contest"""
    RUN_EVERY_DAY = (60*24) # every 24 hours = 1 day

    schedule = Schedule(run_every_mins=RUN_EVERY_DAY)
    code = 'beauty_and_pics.contest_manager_cron_job' # a unique code

    def do(self):
        logger.info("CronJob [ContestManagerJob]: esecuzione cron in corso...")
        contest_obj = Contest()
        # contest manager function
        contest_obj.contest_manager()
        logger.info("CronJob [ContestManagerJob]: esecuzione cron in terminata")
        pass

class WeeklyReportJob(CronJobBase):
    """Cron to send weekly contest report"""
    RUN_EVERY_7DAY = (60*24*7) # every 7 days

    schedule = Schedule(run_every_mins=RUN_EVERY_7DAY)
    code = 'beauty_and_pics.contest_report_cron_job' # a unique code

    def do(self):
        logger.info("CronJob [WeeklyReportJob]: esecuzione cron in corso...")
        contest_obj = Contest()
        contest_obj.contest_report()
        logger.info("CronJob [WeeklyReportJob]: esecuzione cron in terminata")
        pass
