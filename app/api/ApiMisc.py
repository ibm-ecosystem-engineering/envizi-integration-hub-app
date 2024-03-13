from flask import Blueprint, jsonify, request, current_app, send_file,jsonify
import os
import logging
from xml.dom.minidom import Document 
from flask_basicauth import BasicAuth
from flask_login import login_required, fresh_login_required

apiMisc = Blueprint('api_misc', __name__)

@apiMisc.route('/api/v1/welcome', methods=['GET'])
def welcome_api():
    logging.info("welcome ...")
    resp = {"result": "Welcome !!!"}
    logging.info(resp)
    return resp, 200