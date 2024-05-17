
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import tempfile
import sys
import os, json
from util.DateUtils import DateUtils

class FileUtil :

    def __init__(
        self
    ) -> None:
        self._init_config()

    def _init_config(self):
        load_dotenv()
        self.counter = 0
        self.timestampString = ""
        self.fileRootFolder = ""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    def writeInFile(self, fileName, fileText):
        file = open(fileName,"w")
        file.write(fileText)
        file.close()
        return None
    
    def start(self):
        self.counter = 0
        ### Interim files
        WRITE_INTERIM_FILES = os.environ.get('WRITE_INTERIM_FILES', 'FALSE').upper()
        if WRITE_INTERIM_FILES == "FALSE":
            self.write_interim_files = False
            print("The string is 'FALSE'")
        else:
            self.write_interim_files = True
            print("The string is not 'FALSE'")

        self.timestampString = DateUtils.getCurrentDateTimeString()

        temp_folder = tempfile.gettempdir()

        filePath = os.environ.get('OUTPUT_FOLDER', temp_folder)
        filePath = os.path.join(filePath, "results-" + self.timestampString)
        self.logger.info("Output folder : %s " % filePath)

        ### Create folder
        try:
            os.makedirs(filePath)
            self.logger.info("Folder %s created!" % filePath)
            self.fileRootFolder = filePath
        except Exception as e:
            self.logger.error(f' Error in creating folder : {e} ')

    def writeInFileWithCounter(self, fileName, fileText):
        if (self.write_interim_files == True) :
            fileNameWithPath = self.getFileNameWithCounter(fileName)
            self.writeInFile(fileNameWithPath, fileText)
        return None

    def getFileName(self, fileNamePrefix, fileName):
        fileNameWithPath = os.path.join(self.fileRootFolder, fileNamePrefix + fileName)
        self.logger.debug("fileNameWithPath :" + fileNameWithPath)
        return fileNameWithPath

    def getFileNameWithCounter(self, fileName):
        self.counter = self.counter + 1    
        fileNamePrefix = str(self.counter).zfill(4) + "-"
        return self.getFileName (fileNamePrefix, fileName)

    def getFileNameWithoutCounter(self, fileName):
        return self.getFileName ("", fileName)

    def extractFilename(filepath):
        return os.path.basename(filepath)
    

    def loadJsonFileContent(self, fileName):
        self.logger.info("loadJsonFileContent  ... :  " + fileName)
        data = {}
        try:
            with open(fileName, "r") as json_file:
                data = json.load(json_file)
                self.logger.debug(data)
        except FileNotFoundError:
            self.logger.error(f"The file '{fileName}' does not exist.")
        except json.JSONDecodeError:
            self.logger.error(f"The file '{fileName}' is not valid JSON.")

        return data