
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
        self.jobFolder = ""
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
        else:
            self.write_interim_files = True

        self.timestampString = DateUtils.getCurrentDateTimeString()

        temp_folder = tempfile.gettempdir()

        filePath = os.environ.get('OUTPUT_FOLDER', temp_folder)
        filePath = os.path.join(filePath, "results-" + self.timestampString)
        self.logger.info("Output folder : %s " % filePath)

        ### Create folder
        try:
            os.makedirs(filePath)
            self.logger.info("Output Folder %s created!" % filePath)
            self.fileRootFolder = filePath
        except Exception as e:
            self.logger.error(f' Error in creating Output folder : {e} ')

        # temp_folder = tempfile.gettempdir()

        # jobFolderPath = os.environ.get('JOB_FOLDER', temp_folder)
        # self.logger.info("jobFolderPath folder : %s " % filePath)
        # ### Create folder
        # try:
        #     os.makedirs(jobFolderPath)
        #     self.logger.info("Folder %s created!" % jobFolderPath)
        #     self.jobFolder = jobFolderPath
        # except Exception as e:
        #     self.logger.error(f' Error in creating folder : {e} ')


    def writeInFileWithCounter(self, fileName, fileText):
        if (self.write_interim_files == True) :
            fileNameWithPath = self.getFileNameWithCounter(fileName)
            self.writeInFile(fileNameWithPath, fileText)
        return None

    def getFileName(self, fileNamePrefix, fileName):
        fileNameWithPath = os.path.join(self.fileRootFolder, fileNamePrefix + fileName)
        # self.logger.debug("fileNameWithPath :" + fileNameWithPath)
        return fileNameWithPath

    def getFileNameWithCounter(self, fileName):
        self.counter = self.counter + 1    
        fileNamePrefix = str(self.counter).zfill(4) + "-"
        return self.getFileName (fileNamePrefix, fileName)

    def getFileNameWithoutCounter(self, fileName):
        return self.getFileName ("", fileName)

    def extractFilename(filepath):
        return os.path.basename(filepath)
    

    def retrive_file_names_in_folder(self, folder_path):
        files = []
        try:
            for file in os.listdir(folder_path) :
                file_with_path = os.path.join(folder_path, file)
                if os.path.isfile(file_with_path) :
                    files.append(file_with_path)
        except Exception:
            self.logger.error(f"Error in retriving files from '{folder_path}' ")

        self.logger.debug(f"retrive_file_names_in_folder  ... : {files} ")

        return files
    

    def retrive_image_pdf_file_names_in_folder(self, folder_path):
        valid_extensions = ['.pdf','.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        all_files = self.retrive_file_names_in_folder(folder_path)

        files = []
        try:
            for file in all_files :
                file_extension = os.path.splitext(file)[1].lower()
                if file_extension in valid_extensions:
                    files.append(file)
        except Exception:
            self.logger.error(f"Error in retriving file extension '{folder_path}' ")

        self.logger.debug(f"retrive_image_pdf_file_names_in_folder  ... : {files} ")

        return files
    
