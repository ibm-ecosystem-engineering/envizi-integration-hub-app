from dotenv import load_dotenv
from docling.document_converter import DocumentConverter
import os
from dotenv import load_dotenv

import logging 
from util.FileUtil import FileUtil
from util.ConfigUtil import ConfigUtil



import requests

class DoclingMain(object):

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
        self.converter = DocumentConverter()

    def extract_data_from_pdf(self, pdf_file_name):
        result = self.converter.convert(pdf_file_name)
        markdown_output =  result.document.export_to_markdown()
        return markdown_output