import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

from typing import Dict, Optional, Any, Iterable, List
import uuid

import logging 
import os, json

from util.DateUtils import DateUtils
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil
from util.ExcelUtil import ExcelUtil
from excel.ExcelProcessor import ExcelProcessor

class ExcelProS3(object):

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
        self.excelUtil = ExcelUtil()
        self.excelProcessor = ExcelProcessor(self.fileUtil, self.configUtil)


    def createPOC_and_Push_to_s3(self, file_prefix, sheet_name, processed_data) : 
        # Specify the filename for the new Excel file
        output_filename = file_prefix + DateUtils.getSimpleCurrentDateTimeString() + ".xlsx"
        fileNameWithPath = self.fileUtil.getFileNameWithoutCounter(output_filename)

        self.logger.info("createPOC_and_Push_to_s3 uploaded fileName ... : " + output_filename)
        self.fileUtil.writeInFileWithCounter("createPOC_and_Push_to_s3-1-result.json", json.dumps(processed_data))

        # Write the processed DataFrame to a new Excel file
        self.excelUtil.generateExcel(fileNameWithPath, sheet_name, processed_data)

        ### Push file to S3
        s3FileName = self.excelProcessor.pushFileToS3(fileNameWithPath)

        ### Generate Response
        resp = {
                "uploadedFile" : fileNameWithPath,
                "s3FileName" : s3FileName,
                "data" : processed_data,
                "msg": "The file " + fileNameWithPath + " is pushed to s3 successfully."
                }
        
        return resp
