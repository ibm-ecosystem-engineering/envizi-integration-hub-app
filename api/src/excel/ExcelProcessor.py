import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv
import pandas as pd

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

class ExcelProcessor(object):

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

    def pushFileToS3(self, fileNameWithPathToSend):

        ### S3 filename
        s3FileName = FileUtil.extractFilename(fileNameWithPathToSend)
        self.logger.debug(f"S3 File Name :  {s3FileName} ")

        ### push excel file to S3
        s3Main = S3Main(self.configUtil)
        s3Main.pushFileToS3(fileNameWithPathToSend, s3FileName)

        return s3FileName

    