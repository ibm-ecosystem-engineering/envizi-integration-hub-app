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

class ExcelProDB(object):

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
        self.EXCELPRO_FOLDER = self.DATA_STORE_FOLDER + "/excelpro/"
        self.EXCELPRO_FILE = self.EXCELPRO_FOLDER + "/excelpro.json"


    def getExcelProDetailFileName(self, id):
        result = self.EXCELPRO_FOLDER + "/excelpro-" + str(id) + ".json"
        self.logger.info("getExcelProDetailFileName : " + result)
        return result
    

    def loadExcelProMasterFileContent(self):
        self.logger.info("loadExcelProMasterFileContent  ... ")
        data = {}
        try:
            fileName = self.EXCELPRO_FILE
            with open(fileName, "r") as json_file:
                data = json.load(json_file)
                self.logger.debug(data)
        except FileNotFoundError:
            self.logger.error(f"The file '{fileName}' does not exist.")
        except json.JSONDecodeError:
            self.logger.error(f"The file '{fileName}' is not valid JSON.")

        return data

    def loadExcelProDetailById(self, id):
        fileName = self.getExcelProDetailFileName(id)
        excelpro_detail_data = self.fileUtil.loadJsonFileContent(fileName)
        return excelpro_detail_data

    def saveExcelProMaster(self, payload):
        self.logger.info("saveExcelProMaster  ... ")

        ### Retrieve existing content
        data_master = self.loadExcelProMasterFileContent()
        
        ### Write current data in ouput file
        self.fileUtil.writeInFileWithCounter("excelpro-1-before.json", json.dumps(data_master))
        self.fileUtil.writeInFileWithCounter("excelpro-2-to-add.json", json.dumps(payload))

        ### Get or Generate Id
        id = DictionaryUtil.getValue_key1(payload, "id", "")
        if (id == "") :
            id = "EX-" + DateUtils.getSimpleCurrentDateTimeString()

        ### Delete existing master entry
        data_master = [record for record in data_master if record['id'] != id]

        ### ExcelPro master entry 
        ### ---------------------
        mydata = {
            "id": id,
            "name": payload["name"],
            "desc":  payload["desc"],
            "type":  payload["envizi_template"]
        }
        ### add new content in the master
        data_master.append(mydata)
        
        ### Write updated content in the excelpro file
        self.fileUtil.writeInFile(self.EXCELPRO_FILE, json.dumps(data_master))

        ### Write updated data in ouput file
        self.fileUtil.writeInFileWithCounter("saveExcelProMaster-final.json", json.dumps(data_master))

        return id
    

    def saveExcelProDetail(self, payload):
        self.logger.info("saveExcelProDetail  ... ")
    
        id = DictionaryUtil.getValue_key1(payload, "id", "")

        fileName = self.EXCELPRO_FOLDER + "/excelpro-" + id + ".json"
        
        ### create content in the excelpro file
        self.fileUtil.writeInFile(fileName, json.dumps(payload))

        ### Write  data in ouput file
        self.fileUtil.writeInFileWithCounter("saveExcelProDetail-detail.json", json.dumps(payload))

        ### Retrive from DB
        resp = self.loadExcelProDetailById(id)

        return resp
    
   
    def deleteExcelPro(self, payload):
        self.logger.info("deleteExcelPro  ... ")

        ### id
        id = payload["id"]
        
        ### delete master
        data_master = self.deleteExcelProMaster(id)

        ### delete detail
        self.deleteExcelProDetail(id)

        return data_master 
    

    def deleteExcelProMaster(self, id):
        self.logger.info("deleteExcelPro  ... ")

        ### Retrieve existing content
        data_master = self.loadExcelProMasterFileContent()
        
        ### Write current data in ouput file
        self.fileUtil.writeInFileWithCounter("excelpro-1-before.json", json.dumps(data_master))
        self.fileUtil.writeInFileWithCounter("excelpro-2-to-add.json", json.dumps(id))

        data_master = [record for record in data_master if record['id'] != id]

        ### Write updated data in ouput file
        self.fileUtil.writeInFileWithCounter("excelpro-3-final.json", json.dumps(data_master))

        ### Write updated content in the excelpro file
        self.fileUtil.writeInFile(self.EXCELPRO_FILE, json.dumps(data_master))

        return data_master 
    
    def deleteExcelProDetail(self, id):
        self.logger.info("deleteExcelProDetail  ... ")

        ### Remove the excelpro detail file
        fileName = self.getExcelProDetailFileName(id)
        os.remove(fileName)

        return True