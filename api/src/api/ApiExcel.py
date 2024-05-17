from flask import Blueprint, jsonify, request, current_app, send_file
import os
import json
import logging
from xml.dom.minidom import Document 
import pandas as pd

from util.FileUtil import FileUtil
from excel.ExcelMain import ExcelMain

apiExcel = Blueprint('api_excel', __name__)

@apiExcel.route('/api/excel/uploadConfigConnector', methods=['POST'])
def excel_uploadConfigConnector():
    logging.info("welcome uploadConfigConnector...")

    if 'file' not in request.files:
        resp = {"result": "No file part"}
    else:
        file = request.files['file']

        resp = createInstanceExcelMain().uploadConfigConnector(file)
    return resp, 200


@apiExcel.route('/api/excel/loadTemplatePOC', methods=['POST'])
def excel_loadTemplatePOC():
    logging.info("welcome loadTemplatePOC...")

    if 'file' not in request.files:
        resp = {"result": "No file part"}
    else:
        file = request.files['file']

        resp = createInstanceExcelMain().loadTemplatePOC(file)
    return resp, 200


@apiExcel.route('/api/excel/ingestTemplatePOC', methods=['POST'])
def excel_ingestTemplatePOC():
    logging.info("welcome ingestTemplatePOC...")

    ### Update the config data
    payload = request.get_json()

    template_columns = payload["template_columns"]
    uploaded_columns = payload["uploaded_columns"]
    uploadedFile = payload["uploadedFile"]
    data_mapping = payload["data_mapping"]

    resp = createInstanceExcelMain().ingestTemplatePOC(template_columns, uploaded_columns, uploadedFile, data_mapping)
    return resp, 200


@apiExcel.route('/api/excel/loadTemplateASDL', methods=['POST'])
def excel_loadTemplateASDL():
    logging.info("welcome loadTemplateASDL...")

    if 'file' not in request.files:
        resp = {"result": "No file part"}
    else:
        file = request.files['file']

        resp = createInstanceExcelMain().loadTemplateASDL(file)
    return resp, 200

@apiExcel.route('/api/excel/ingestTemplateASDL', methods=['POST'])
def excel_ingestTemplateASDL():
    logging.info("welcome ingestTemplateASDL...")

    ### Update the config data
    payload = request.get_json()

    template_columns = payload["template_columns"]
    uploaded_columns = payload["uploaded_columns"]
    uploadedFile = payload["uploadedFile"]
    data_mapping = payload["data_mapping"]

    resp = createInstanceExcelMain().ingestTemplateASDL(template_columns, uploaded_columns, uploadedFile, data_mapping)
    return resp, 200

@apiExcel.route('/api/excel/read', methods=['POST'])
def excel_read():
    logging.info("welcome upload...")

    if 'file' not in request.files:
        resp = {"result": "No file part"}
    else:
        file = request.files['file']

        if file.filename == '':
            resp = {"result": "No selected file'"}
        else:
            try:
                # Read Excel file into pandas DataFrame
                df = pd.read_excel(file)
                # Convert DataFrame to JSON
                json_data = df.to_json(orient='records')
                resp = jsonify(json_data)
            except Exception as e:
                return f'Error processing file: {e}', 500
    
    logging.info(resp)
    return resp, 200

def createInstanceExcelMain():
    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### TurboMain
    configUtil = current_app.config["configUtil"]
    excelMain = ExcelMain(fileUtil, configUtil)

    return excelMain
