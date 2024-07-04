from flask import Blueprint, jsonify, request, current_app, send_file
import os
import json
import logging
from xml.dom.minidom import Document 

from util.FileUtil import FileUtil
from excel.ExcelMain import ExcelMain

apiLogin = Blueprint('api_login', __name__)

@apiLogin.route('/api/login/validate', methods=['POST'])
def login_validate():
    logging.info("welcome login_validate...")

    ### Update the config data
    payload = request.get_json()

    username = payload["username"]
    password = payload["password"]

    resp = {}
    resp["username"] = username
    resp["username"] = username

    if (username == "admin" and password == "admin") :
        resp["login_status"] = "TRUE"
        resp["msg"] = "Login success"
    else :
        resp["login_status"] = "FALSE"
        resp["msg"] = "Login failed"
    return resp, 200
