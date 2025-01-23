from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from dotenv import load_dotenv

import os
from util.ConfigUtil import ConfigUtil
from util.DateUtils import DateUtils

import logging

class SchedulerMain(object):

    def __init__(
        self,
        configUtil: ConfigUtil
    ) -> None:
        self.configUtil = configUtil
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self._init_load()

    def _init_load(self):
        self.logger.info("SchedulerMain :  _init_load ... ")
        self.scheduler = BackgroundScheduler()

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info("SchedulerMain :  start error ... ")

    def start(self):
        self.logger.info("SchedulerMain :  start ... ")
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info("SchedulerMain :  start error ... ")

    def stop(self):
        self.logger.info("SchedulerMain :  stop ... ")
        try:
            self.scheduler.stop()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info("SchedulerMain :  stop error ... ")

    def add_interval_job(self, job, job_args, start_date, end_date, interval_minutes, job_id):
        ### Remove the job first
        self.remove_job(job_id)

        trigger = IntervalTrigger(start_date=start_date, end_date=end_date, seconds=interval_minutes)

        ### Add the job
        self.logger.info(f"SchedulerMain :  add_interval_job : {job_id} ")
        self.scheduler.add_job(job,  args=job_args, trigger=trigger, id=job_id)

    def add_cron_job(self, job, job_hour, job_minute, job_id):
        self.logger.info(f"SchedulerMain :  add_cron_job : {job_id} ")
        self.scheduler.add_job(job, trigger=CronTrigger(hour=job_hour, minutes=job_minute), id=job_id)

    def create_job_id (self):
        job_id = "job_" + DateUtils.getCurrentDateTimeString()
        return job_id

    def remove_job (self, job_id):
        self.logger.info(f"SchedulerMain :  remove_job : {job_id} ")
        # Check if the job exists
        job = self.scheduler.get_job(job_id)
        if job:
            self.logger.info(f"SchedulerMain :  Job with id '{job_id}' exists. Removing it...")
            self.scheduler.remove_job(job_id)

    def is_job_running (self, job_id):
        self.logger.debug(f"SchedulerMain :  is_job_running : {job_id} ")
        job = self.scheduler.get_job(job_id)
        result = False
        if job:
            result = True
        return result


