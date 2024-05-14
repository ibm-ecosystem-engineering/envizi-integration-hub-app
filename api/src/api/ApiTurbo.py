from flask import Blueprint, jsonify, request, current_app, send_file
import os
import json
import logging
from xml.dom.minidom import Document 

from util.FileUtil import FileUtil
from turbo.TurboMain import TurboMain

apiTurbo = Blueprint('api_turbo', __name__)

@apiTurbo.route('/api/turbo/queryForIngest', methods=['POST'])
def turbo_queryForIngest():
    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### TurboMain
    configUtil = current_app.config["configUtil"]
    turboMain = TurboMain(fileUtil, configUtil)

    payload = request.get_json()
    resp = turboMain.queryForIngest(payload)
    return resp, 200

@apiTurbo.route('/api/turbo/queryForView', methods=['POST'])
def turbo_queryForView():
    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### TurboMain
    configUtil = current_app.config["configUtil"]
    turboMain = TurboMain(fileUtil, configUtil)

    payload = request.get_json()
    resp = turboMain.queryForView(payload)
    return resp, 200

@apiTurbo.route('/api/turbo/queryForDownload', methods=['POST'])
def turbo_queryForDownload():
    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### TurboMain
    configUtil = current_app.config["configUtil"]
    turboMain = TurboMain(fileUtil, configUtil)

    payload = request.get_json()
    file_path = turboMain.queryForDownload(payload)
    return send_file(file_path, as_attachment=True)
