import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import logging 
import os, json

from util.DateUtils import DateUtils
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.DictionaryUtil import DictionaryUtil
from util.JsonUtil import JsonUtil

from CommonConstants import *

class SchedulerDB(object):

    def __init__(
        self,
        fileUtil: FileUtil,
        configUtil: ConfigUtil
    ) -> None:
        self.fileUtil = fileUtil
        self.configUtil = configUtil
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self._init_config()

    def _init_config(self):
        self.DATA_STORE_FOLDER = os.getenv("DATA_STORE_FOLDER") 
        self.SCHEDULAR_FOLDER = self.DATA_STORE_FOLDER + "/schedular/"
        self.SCHEDULAR_STATUS_FOLDER = self.DATA_STORE_FOLDER + "/schedular_status/"

    def loadJobFileContent(self, scheduler_type, job_id):
        ### Get the file name
        file_name = self.get_job_status_file(scheduler_type, job_id)

        data = JsonUtil.loadJsonArrayFileContent(file_name)
        return data
    
    def loadJobFileContentColumns(self, scheduler_type):
        mydata = [ "record_id", "start_datetime", "end_datetime", "status"]
        return mydata

    def get_job_status_file (self, scheduler_type, job_id):
        self.logger.info("SchedulerDB : create_job_status_file  ")

        ### Create status file folder
        folder_path = self.SCHEDULAR_STATUS_FOLDER + "/" + scheduler_type  + "/" + job_id  
        os.makedirs(folder_path, exist_ok=True)

        file_name = folder_path + "/status_" + DateUtils.getCurrentDateString()  + ".json" 
        
        return file_name


    def create_job_started_entry (self, scheduler_type, job_id):
        # self.logger.info("SchedulerDB : create_job_started_entry  ")

        ### Get the file name
        file_name = self.get_job_status_file(scheduler_type, job_id)

        ### ---------------------
        job_status_data = {
            "record_id": "Id-" + DateUtils.getCurrentDateTimeString(),
            "start_datetime": DateUtils.getCurrentDateTimeString2(),
            "end_datetime": "",
            "status": SCHEDULER_STATUS_IN_PROGRESS,
        }
        ### Write the status
        JsonUtil.add_record_to_json_file(file_name, job_status_data)

        mydata = {
            "job_status_file_name": file_name,
            "job_status_data": job_status_data,
        }
        return mydata
    
    def update_job_completed_entry (self, mydata):
        # self.logger.info("SchedulerDB : create_job_completed_entry  ")

        job_status_file_name = mydata ["job_status_file_name"]
        job_status_data = mydata ["job_status_data"]
        
        record_id = job_status_data ["record_id"]

        end_datetime = DateUtils.getCurrentDateTimeString2()

        JsonUtil.update_record_to_json_file(job_status_file_name, "record_id", record_id, "end_datetime", end_datetime, "status", SCHEDULER_STATUS_COMPLETED)

        return mydata