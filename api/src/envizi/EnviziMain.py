import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

from typing import Dict, Optional, Any, Iterable, List
import uuid
import requests

# import getpass
import logging 
import os, json

from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.DictionaryUtil import DictionaryUtil

class EnviziMain(object):

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
        self.init_config()

    def init_config(self):
        ENVIZI_API_URL = self.configUtil.ENVIZI_API_URL
        ENVIZI_API_TOKEN = self.configUtil.ENVIZI_API_TOKEN


    def callEnviziAPI(self, api_label, api_url, token):
        self.logger.debug(f"---------------------------- Envizi API : {api_label} : ---------------------------- ")
        self.logger.debug(f" api_url : {api_url}")

        myheaders = {   
            'Authorization': f'Bearer {token}'
        }

        ###Log the post content
        response = requests.get(api_url, headers=myheaders)
        resp = self._processApiResponse(api_label, response)

        self.logger.debug(f"----------------------------  ---------------------------- ")
        return resp


    def _processApiResponse(self, api_label, response):
        self.fileUtil.writeInFileWithCounter(api_label + ".json", json.dumps(response.json()))

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            resp = response.json()
        else:
            # Print an error message if the request was not successful
            self.logger.error(f"API {api_label} : request failed with status code {response.status_code} : {response.text}")
            resp = {}
        return resp
    

    def exportLocation(self):
        self.logger.info("exportLocation  ... ")

        resp = {}
        try:
            url = self.configUtil.ENVIZI_API_URL + "/data/_Envizi-SetupLocations"
            token = self.configUtil.ENVIZI_API_TOKEN

            result = self.callEnviziAPI("Locations", url, token )
            list = [item["Location Name"] for item in result]

            resp["data"] = list
            resp["msg"] = "The locations are retrived successfully"

        except Exception as e:
            self.logger.info(f' Unable to retrive locations : {e} \n\n')
            resp["data"] = []
            resp["msg"] = "Unable to retrive locations"

        return resp
    
    def exportAccounts(self):
        self.logger.info("exportAccounts  ... ")

        resp = {}
        try:
            url = self.configUtil.ENVIZI_API_URL + "/data/_Envizi-SetupAccounts"
            token = self.configUtil.ENVIZI_API_TOKEN

            result = self.callEnviziAPI("Accounts", url, token )
            list = [item["Account Number"] for item in result]

            resp["data"] = list
            resp["msg"] = "The accounts are retrived successfully"

        except Exception as e:
            self.logger.info(f' Unable to retrive accounts : {e} \n\n')
            resp["data"] = []
            resp["msg"] = "Unable to retrive accounts"

        return resp
