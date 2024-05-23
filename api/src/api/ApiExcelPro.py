from flask import Blueprint, jsonify, request, current_app, send_file
import os
import json
import logging
from xml.dom.minidom import Document 
import pandas as pd

from util.FileUtil import FileUtil
from excelpro.ExcelProMain import ExcelProMain

apiExcelPro = Blueprint('api_excel_pro', __name__)

def createInstanceExcelProMain():
    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### TurboMain
    configUtil = current_app.config["configUtil"]
    excelMain = ExcelProMain(fileUtil, configUtil)

    return excelMain


@apiExcelPro.route('/api/excelpro/loadall', methods=['POST'])
# @auth.login_required
def excelpro_loadall():
    logging.info("welcome excelpro_loadall...")
    resp = createInstanceExcelProMain().loadAll()
    return resp, 200


@apiExcelPro.route('/api/excelpro/uploadData', methods=['POST'])
def excel_uploadData():
    logging.info("welcome uploadData...")

    if 'file' not in request.files:
        resp = {"result": "No file part"}
    else:
        file = request.files['file']
        envizi_template = request.form['envizi_template']

    # payload = request.get_json()
    # envizi_template = payload["envizi_template"]

    resp = createInstanceExcelProMain().uploadData(file, envizi_template)
    return resp, 200


@apiExcelPro.route('/api/excelpro/ingestToEnvizi', methods=['POST'])
def excel_ingestToEnvizi():
    logging.info("welcome ingestToEnvizi...")

    ### Update the config data
    payload = request.get_json()

    uploadedFile = payload["uploadedFile"]
    main_data = payload["main_data"]

    resp = createInstanceExcelProMain().ingestToEnvizi(main_data, uploadedFile)
    return resp, 200


@apiExcelPro.route('/api/excelpro/viewInScreen', methods=['POST'])
def excel_viewInScreen():
    logging.info("welcome viewInScreen...")

    ### Update the config data
    payload = request.get_json()

    uploadedFile = payload["uploadedFile"]
    main_data = payload["main_data"]

    resp = createInstanceExcelProMain().viewInScreen(main_data, uploadedFile)
    return resp, 200


@apiExcelPro.route('/api/excelpro/load', methods=['POST'])
def excelpro_load():
    logging.info("welcome excelpro_load...")

    ### Get Payload
    payload = request.get_json()

    ### Load
    resp = createInstanceExcelProMain().loadExcelPro(payload)

    return resp, 200

@apiExcelPro.route('/api/excelpro/loadnew', methods=['POST'])
def excelpro_loadnew():
    logging.info("welcome excelpro_loadnew...")

    ### Get Payload
    payload = request.get_json()

    ### Load
    resp = createInstanceExcelProMain().loadExcelProNew(payload)

    return resp, 200

@apiExcelPro.route('/api/excelpro/templatechange', methods=['POST'])
def excelpro_templatechange():
    logging.info("welcome excelpro_templatechange...")

    ### Get Payload
    payload = request.get_json()

    ### Load
    resp = createInstanceExcelProMain().loadExcelProTemplateChange(payload)

    return resp, 200

@apiExcelPro.route('/api/excelpro/save', methods=['POST'])
def excelpro_save():
    logging.info("welcome excelpro_save...")

    ### Get Payload
    payload = request.get_json()

    ### Add
    resp = createInstanceExcelProMain().saveExcelPro(payload)

    return resp, 200

@apiExcelPro.route('/api/excelpro/delete', methods=['POST'])
def excelpro_delete():
    logging.info("welcome excelpro_delete...")

    ### Get Payload
    payload = request.get_json()

    ### Load
    resp = createInstanceExcelProMain().deleteExcelPro(payload)

    return resp, 200

@apiExcelPro.route('/api/excelpro/read', methods=['POST'])
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