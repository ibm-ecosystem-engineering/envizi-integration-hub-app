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

from CommonConstants import *

class WebhookDB(object):

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
        self.WEBHOOK_FOLDER = self.DATA_STORE_FOLDER + "/webhook/"
        self.WEBHOOK_FILE = self.WEBHOOK_FOLDER + "/webhook.json"


    def getWebhookDetailFileName(self, id):
        result = self.WEBHOOK_FOLDER + "/webhook-" + str(id) + ".json"
        self.logger.info("getWebhookDetailFileName : " + result)
        return result
    

    def loadWebhookMasterFileContent(self):
        self.logger.info("loadWebhookMasterFileContent  ... ")
        data = {}
        try:
            fileName = self.WEBHOOK_FILE
            with open(fileName, "r") as json_file:
                data = json.load(json_file)
                self.logger.debug(data)
        except FileNotFoundError:
            self.logger.error(f"The file '{fileName}' does not exist.")
        except json.JSONDecodeError:
            self.logger.error(f"The file '{fileName}' is not valid JSON.")

        return data

    def loadWebhookDetailById(self, id):
        fileName = self.getWebhookDetailFileName(id)
        webhook_detail_data = self.fileUtil.loadJsonFileContent(fileName)
        return webhook_detail_data

    def saveWebhookMaster(self, payload):
        self.logger.info("saveWebhookMaster  ... ")

        ### Retrieve existing content
        data_master = self.loadWebhookMasterFileContent()
        
        ### Write current data in ouput file
        self.fileUtil.writeInFileWithCounter("webhook-1-before.json", json.dumps(data_master))
        self.fileUtil.writeInFileWithCounter("webhook-2-to-add.json", json.dumps(payload))

        ### Get or Generate Id
        id = DictionaryUtil.getValue_key1(payload, "id", "")
        if (id == "") :
            id = "WH-" + DateUtils.getSimpleCurrentDateTimeString()

        ### Delete existing master entry
        data_master = [record for record in data_master if record['id'] != id]

        ### Webhook master entry 
        ### ---------------------
        mydata = {
            "id": id,
            "name": payload["name"],
            "desc":  payload["desc"],
            "type":  payload["envizi_template"]
        }
        ### add new content in the master
        data_master.append(mydata)
        
        ### Write updated content in the webhook file
        self.fileUtil.writeInFile(self.WEBHOOK_FILE, json.dumps(data_master))

        ### Write updated data in ouput file
        self.fileUtil.writeInFileWithCounter("saveWebhookMaster-final.json", json.dumps(data_master))

        return id
    

    def saveWebhookDetail(self, payload):
        self.logger.info("saveWebhookDetail  ... ")
    
        id = DictionaryUtil.getValue_key1(payload, "id", "")

        fileName = self.WEBHOOK_FOLDER + "/webhook-" + id + ".json"
        
        ### create content in the webhook file
        self.fileUtil.writeInFile(fileName, json.dumps(payload))

        ### Write  data in ouput file
        self.fileUtil.writeInFileWithCounter("saveWebhookDetail-detail.json", json.dumps(payload))

        ### Retrive from DB
        resp = self.loadWebhookDetailById(id)

        return resp
    
   
    def deleteWebhook(self, payload):
        self.logger.info("deleteWebhook  ... ")

        ### id
        id = payload["id"]
        
        ### delete master
        data_master = self.deleteWebhookMaster(id)

        ### delete detail
        self.deleteWebhookDetail(id)

        return data_master 
    

    def deleteWebhookMaster(self, id):
        self.logger.info("deleteWebhook  ... ")

        ### Retrieve existing content
        data_master = self.loadWebhookMasterFileContent()
        
        ### Write current data in ouput file
        self.fileUtil.writeInFileWithCounter("webhook-1-before.json", json.dumps(data_master))
        self.fileUtil.writeInFileWithCounter("webhook-2-to-add.json", json.dumps(id))

        data_master = [record for record in data_master if record['id'] != id]

        ### Write updated data in ouput file
        self.fileUtil.writeInFileWithCounter("webhook-3-final.json", json.dumps(data_master))

        ### Write updated content in the webhook file
        self.fileUtil.writeInFile(self.WEBHOOK_FILE, json.dumps(data_master))

        return data_master 
    
    def deleteWebhookDetail(self, id):
        self.logger.info("deleteWebhookDetail  ... ")

        ### Remove the webhook detail file
        fileName = self.getWebhookDetailFileName(id)
        os.remove(fileName)

        return True
    

    