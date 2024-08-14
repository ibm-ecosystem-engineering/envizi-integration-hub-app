import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import requests
import logging 
import os, json


from util.MathUtil import MathUtil

from util.DateUtils import DateUtils
from util.DictionaryUtil import DictionaryUtil
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.ExcelUtil import ExcelUtil
from s3.S3Main import S3Main

from datetime import datetime
from datetime import timedelta

from turbo.TurboApi import TurboApi
from turbo.TurboUtil import TurboUtil

class TurboProcessor(object):

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
        self.turboApi = TurboApi(self.fileUtil, self.configUtil)

    def turboLogin(self, payload):
        self.logger.info(f"---------------------------- Querying Turbonomic for Login : ---------------------------- ")
        resp = self.turboApi.turboLogin(payload)
        return resp
    
    def queryTurboDataCenter(self, payload, sessionid):
        self.logger.info(f"---------------------------- Querying Turbonomic for DataCenter Data : ---------------------------- ")
        resp = self.turboApi.queryTurboDataCenter(payload, sessionid)
        return resp

    def queryTurboRegion(self, payload, sessionid):
        self.logger.info(f"---------------------------- Querying Turbonomic for Region Data : ---------------------------- ")
        resp = self.turboApi.queryTurboRegion(payload, sessionid)
        return resp
    
    def queryTurboForAccounts(self, payload, sessionid, startDate, endDate):
        self.logger.info(f"---------------------------- Querying Turbonomic for Accounts Data : ---------------------------- ")

        ### Accounts and Data
        dataCenterJson = self.turboApi.queryTurboDataCenterForAccounts(payload, sessionid)

        myAccounts = {
            "energy_consumption": [], 
            "active_hosts": [], 
            "active_vms": [], 
            "energy_host_intensity": [], 
            "vm_host_density": []
            }
        
        ### For each Dates
        num_days = (endDate - startDate).days
        self.logger.info(f"Processing num_days --> {num_days}" )
        for i in range(num_days + 1):
            processing_date = startDate + timedelta(days=i)
            processing_date_string = DateUtils.dateToString(processing_date)
            self.logger.info(f"Processing for the date --> {processing_date_string}" )

            ### For each DataCenter
            for row in dataCenterJson:
                myuuid = row["uuid"]

                self.logger.info(f"Processing for the datacenter --> {myuuid}" )

                ### Supply Chain
                api_url = self.configUtil.TURBO_URL + "/api/v3/supplychains?environment_type=ONPREM&uuids=" + myuuid
                supplychainsJson = self.turboApi.callTurboAPI ("supplychains-" + myuuid, api_url, payload, sessionid)

                ### Entity Stats
                entityPayload = {
                    "startDate": processing_date_string + "T00:00:01+00:00",
                    "endDate": processing_date_string + "T23:59:59+00:00",
                    "statistics": [
                        {
                            "name": "Energy",
                            "filters": [
                                {
                                    "type": "relation",
                                    "value": "sold"
                                }
                            ]
                        }
                    ]
                }
                api_url = self.configUtil.TURBO_URL + "/api/v3/entities/" + myuuid + "/stats" 
                entitiesJson = self.turboApi.callTurboPostAPI ("entities-" + myuuid, api_url, entityPayload, sessionid)

                ### Account values
                activeHostCount = DictionaryUtil.getValue_key4 (supplychainsJson, "seMap", "PhysicalMachine", "stateSummary", "ACTIVE", 0)
                energyConsumption = TurboUtil.findEnergyConsumption(entitiesJson)
                energyToHostIntensity = round(MathUtil.divide(energyConsumption, activeHostCount), 4)
                vMCount = DictionaryUtil.getValue_key4 (supplychainsJson, "seMap", "VirtualMachine", "stateSummary", "ACTIVE", 0)
                vMToHostDensity = round(MathUtil.divide(vMCount, activeHostCount), 4)

                ### Common values...
                location = DictionaryUtil.getValue_key1 (row, "displayName", "")
                location = DictionaryUtil.getValue_key2_index (row, "tags", "EnviziAlternateName", 0, location)

                ### Records
                # myAccounts.append(self._createAccountRecord(location, "Active Hosts [Number]", "Active Hosts", processing_date_string, activeHostCount))
                # myAccounts.append(self._createAccountRecord(location, "Energy Consumption - kWh", "Energy Consumption", processing_date_string, energyConsumption))
                # myAccounts.append(self._createAccountRecord(location, "Energy Host Intensity - kWh/host", "Energy Host Intensity", processing_date_string, energyToHostIntensity))
                # myAccounts.append(self._createAccountRecord(location, "Active Virtual Machines [Number]", "Active VMs", processing_date_string, vMCount))
                # myAccounts.append(self._createAccountRecord(location, "Virtual Machine to Host Density - VM/Host", "VM Host Density", processing_date_string, vMToHostDensity))

                account_style = self.configUtil.getAccountStyleInfo("energy_consumption")
                myRow = self._createAccountRecordFull(account_style, location, processing_date_string, energyConsumption)
                myAccounts["energy_consumption"].append(myRow)
        
                account_style = self.configUtil.getAccountStyleInfo("active_hosts")
                myRow = self._createAccountRecordFull(account_style, location, processing_date_string, activeHostCount)
                myAccounts["active_hosts"].append(myRow)

                account_style = self.configUtil.getAccountStyleInfo("active_vms")
                myRow = self._createAccountRecordFull(account_style, location, processing_date_string, vMCount)
                myAccounts["active_vms"].append(myRow)

                account_style = self.configUtil.getAccountStyleInfo("energy_host_intensity")
                myRow = self._createAccountRecordFull(account_style, location, processing_date_string, energyToHostIntensity)
                myAccounts["energy_host_intensity"].append(myRow)

                account_style = self.configUtil.getAccountStyleInfo("vm_host_density")
                myRow = self._createAccountRecordFull(account_style, location, processing_date_string, vMToHostDensity)
                myAccounts["vm_host_density"].append(myRow)

        return myAccounts

        
    def writeDataInS3(self, myData, myLabel, excel_sheet_name, excel_file_prefix, ingestFlag):
        ### Write in json file..just for reference
        self.fileUtil.writeInFileWithCounter(myLabel + ".json", json.dumps(myData))

        ### S3 filename
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y%m%d-%H%M%S")
        s3FileName = excel_file_prefix + self.configUtil.ENVIZI_PREFIX + "_" + timestamp + ".xlsx"
        self.logger.debug(f"S3 File Name :  {s3FileName} ")

        ### Write in excel file
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(s3FileName)
        self.logger.info(f" Generate Excel file  :  {fileNameWithPath} ")

        excelUtil = ExcelUtil()
        excelUtil.generateExcel(fileNameWithPath, excel_sheet_name, myData)

        ### push excel file to S3
        s3Main = S3Main(self.configUtil)
        if ingestFlag :
            s3Main.pushFileToS3(fileNameWithPath, s3FileName)

        return fileNameWithPath


    def createLocationData(self, dataCenterJson):
        myLocations = []
            
        for row in dataCenterJson:
            myRow = {}
            myRow["ORGANIZATION"] = self.configUtil.ENVIZI_ORG_NAME
            myRow["GROUP TYPE"] = "Portfolio"
            myRow["GROUP HIERARCHY NAME"] = ""
            myRow["GROUP NAME 1"] = self._appendTurboPrefix(self.configUtil.TURBO_GROUP_NAME)
            myRow["GROUP NAME 2"] = self._appendTurboPrefix(self.configUtil.TURBO_SUB_GROUP_NAME)
            myRow["GROUP NAME 3"] = self._appendTurboPrefix( row["environmentType"] + "_" +  row["className"])
            # LOCATION = tags.EnviziAlternateName[0] ? tags.EnviziAlternateName[0] : displayName
            myRow["LOCATION"] = self._appendTurboPrefix( row["displayName"] )
            myRow["LOCATION TYPE"] = ""
            myRow["LOCATION REFERENCE"] = self._appendTurboPrefix( row["uuid"] )

            myRow["LOCATION REF NO"] = None
            myRow["LOCATION ID"] = ""
            myRow["STREET ADDRESS"] = None
            myRow["CITY"] = None
            myRow["STATE PROVINCE"] = None
            myRow["POSTAL CODE"] = None

            # LONGITUDEX = region#aspects.regionAspect.longitude ? region#aspects.regionAspect.longitude : tags.Longitude[0]
            # LATITUDEY = region#aspects.regionAspect.latitude ? region#aspects.regionAspect.latitude : tags.Latitude[0]
            if "tags" in row:
                myRow["COUNTRY"] = row["tags"]["Country"][0]
                myRow["LATITUDE Y"] = row["tags"] ["Latitude"][0]
                myRow["LONGITUDE X"] = row["tags"]["Longitude"][0]
            else : 
                myRow["COUNTRY"] = None
                myRow["LATITUDE Y"] = None
                myRow["LONGITUDE X"] = None
        
            myRow["LOCATION CLOSE DATE"] = None

            myLocations.append(myRow)

        return myLocations

    def _createAccountRecord(self, location, account_style, account_name, date_string, qty):
        myRow = {}
        myRow["Organization"] = self.configUtil.ENVIZI_ORG_NAME
        myRow["Location"] = self._appendTurboPrefix( location )
        myRow["Account Style Caption"] = account_style
        myRow["Account Number"] = self._appendTurboPrefix( location ) + "_" + account_name
        myRow["Account Reference"] = None
        myRow["Account Supplier"] = "Turbonomic"
        myRow["Record Start YYYY-MM-DD"] = date_string
        myRow["Record End YYYY-MM-DD"] = date_string
        myRow["Quantity"] = qty
        myRow["Total cost (incl. Tax) in local currency"] = None
        myRow["Record Reference"] = None
        myRow["Record Invoice Number"] = None
        myRow["Record Data Quality"] = "Actual"    
        return myRow

    def _createAccountRecordFull(self, account_style, location, date_string, qty):
        myRow = {}

        ### Fixed Columns
        myRow["Organization Link"] = self.configUtil.ENVIZI_ORG_LINK
        myRow["Organization"] = self.configUtil.ENVIZI_ORG_NAME
        myRow["Location"] = self._appendTurboPrefix( location )
        myRow["Location Ref"] = None
        myRow["Account Style Link"] = account_style["link"]
        myRow["Account Style Caption"] = account_style["caption"]
        myRow["Account Subtype"] = ""
        myRow["Account Number"] = self._appendTurboPrefix( location ) + "_" + account_style["account_name"]
        myRow["Account Reference"] = None
        myRow["Account Supplier"] = "Turbonomic"
        myRow["Account Reader"] = None
        myRow["Record Start YYYY-MM-DD"] = date_string
        myRow["Record End YYYY-MM-DD"] = date_string
        myRow["Record Data Quality"] = "Actual"    
        myRow["Record Billing Type"] = None
        myRow["Record Subtype"] = None
        myRow["Record Entry Method"] = None
        myRow["Record Reference"] = None
        myRow["Record Invoice Number"] = None

        ### Additional columns based on account style
        firstRecord = True
        for column in account_style["columns"]:
            if firstRecord:
                firstRecord = False
                myRow[column] = qty
            else:
                myRow[column] = None

        return myRow
        

    def _createAccountRecordCommon(self, organization_link, location, account_style_link, account_style, account_name, date_string):
        myRow = {}
        myRow["Organization Link"] = organization_link
        myRow["Organization"] = self.configUtil.ENVIZI_ORG_NAME
        myRow["Location"] = self._appendTurboPrefix( location )
        myRow["Location Ref"] = None
        myRow["Account Style Link"] = account_style_link
        myRow["Account Style Caption"] = account_style
        myRow["Account Subtype"] = ""
        myRow["Account Number"] = self._appendTurboPrefix( location ) + "_" + account_name
        myRow["Account Reference"] = None
        myRow["Account Supplier"] = "Turbonomic"
        myRow["Account Reader"] = None
        myRow["Record Start YYYY-MM-DD"] = date_string
        myRow["Record End YYYY-MM-DD"] = date_string
        myRow["Record Data Quality"] = "Actual"    
        myRow["Record Billing Type"] = None
        myRow["Record Subtype"] = None
        myRow["Record Entry Method"] = None
        myRow["Record Reference"] = None
        myRow["Record Invoice Number"] = None
        return myRow

    def _populateAccountRecord_EnergyConsumption(self, myRow, qty):
        myRow["Total Electricity (kWh)"] = qty
        myRow["Green Power (kWh)"] = None
        myRow["Total Cost"] = None

    def _populateAccountRecord_ActiveHosts(self, myRow, qty):
        myRow["Active Hosts (Number)"] = qty

    def _populateAccountRecord_ActiveVM(self, myRow, qty):
        myRow["Active Virtual Machines (Number)"] = qty

    def _populateAccountRecord_EnergyHostIntensity(self, myRow, qty):
        myRow["Energy per host (kWh/Host)"] = qty

    def _populateAccountRecord_VMtoHostDensity(self, myRow, qty):
        myRow["Virtual Machine to Host Density (VM/Host)"] = qty

    def _appendTurboPrefix(self, text):
        return self.configUtil.ENVIZI_PREFIX + "-" + text