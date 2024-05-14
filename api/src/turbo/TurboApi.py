import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import requests
import logging 
import os, json

from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil

class TurboApi(object):

    def __init__(
        self,
        fileUtil: FileUtil,
        configUtil: ConfigUtil,
    ) -> None:
        load_dotenv()
        self.fileUtil = fileUtil
        self.configUtil = configUtil
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    def callTurboLoginAPI(self, api_label, api_url):
        self.logger.debug(f"---------------------------- Turbonomic API : {api_label} : ---------------------------- ")
        self.logger.debug(f" api_url : {api_url}")

        login_data = {
            "username": self.configUtil.TURBO_USER,
            "password": self.configUtil.TURBO_PASSWORD
        }
        myheaders = {
            "accept": "application/json"
        }

        # Make an HTTP POST request to the login endpoint with the credentials
        response = requests.post(api_url, headers=myheaders, data=login_data, verify=False)  # You can also use data=login_data if needed
        token = ""
        try:
            rh = response.headers
            token = rh['Set-Cookie'].split(';')[0]
            self.logger.debug(f' Length of the token is : {len(token)} ')
        except Exception as e:
            self.logger.error(f' Error in callTurboLoginAPI : {e} ')
        self.logger.debug(f"----------------------------  ---------------------------- ")
        return token
    
        
    def callTurboPostAPI(self, api_label, api_url, payload, sessionid):
        self.logger.debug(f"---------------------------- Turbonomic API : {api_label} : ---------------------------- ")
        self.logger.debug(f" api_url : {api_url}")

        myheaders = {   
            "cookie": sessionid,
            "accept" : "application/json",
            "Content-Type" : "application/json" 
        }

        ###Log the post content
        fileContent = "api_url : " + api_url
        fileContent = fileContent + "\n\n headers : " + json.dumps(myheaders)
        fileContent = fileContent + "\n\n data : " + json.dumps(payload)
        self.fileUtil.writeInFileWithCounter(api_label + ".txt", fileContent)

        response = requests.post(api_url, headers=myheaders, data=json.dumps(payload), verify=False, stream=True)
        resp = self._processApiResponse(api_label, response)

        self.logger.debug(f"----------------------------  ---------------------------- ")
        return resp
    
    def callTurboAPI(self, api_label, api_url, payload, sessionid):
        self.logger.debug(f"---------------------------- Turbonomic API : {api_label} : ---------------------------- ")
        self.logger.debug(f" api_url : {api_url}")

        fileContent = "api_url : " + api_url
        fileContent = fileContent + "\n\n data : " + str(payload)
        self.fileUtil.writeInFileWithCounter(api_label + ".txt", fileContent)

        myheaders = { "cookie": sessionid }
        response = requests.get(api_url, headers=myheaders, data=payload, verify=False, stream=True)
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

    def turboLogin(self, payload):
        api_url = self.configUtil.TURBO_URL + "/api/v3/login?hateoas=true"
        token = self.callTurboLoginAPI ("Login", api_url)
        return token

    def queryTurboRegion(self, payload, sessionid):
        api_url = self.configUtil.TURBO_URL + "/api/v3/search?detail_type=aspects&types=Region"  # Replace with the actual endpoint you want to access
        resp = self.callTurboAPI ("Region", api_url, payload, sessionid)
        return resp

    def queryTurboDataCenter(self, payload, sessionid):
        self.logger.info(f"---------------------------- Turbonomic Querying for DataCenter Data : ---------------------------- ")

        api_url = self.configUtil.TURBO_URL + "/api/v3/search?detail_type=aspects&types=DataCenter"  # Replace with the actual endpoint you want to access

        resp = self.callTurboAPI ("DataCenter", api_url, payload, sessionid)
        return resp

    def queryTurboDataCenterForAccounts(self, payload, sessionid):
        api_url = self.configUtil.TURBO_URL + "/api/v3/search?types=DataCenter"  # Replace with the actual endpoint you want to access

        resp = self.callTurboAPI ("DataCenter", api_url, payload, sessionid)
        return resp