from flask import Blueprint, jsonify, request, current_app, send_file
import os
import json
import logging
from xml.dom.minidom import Document 

from util.FileUtil import FileUtil
from invoice.InvoiceMain import InvoiceMain

apiInvoice = Blueprint('api_invoice', __name__)

@apiInvoice.route('/api/invoice/export', methods=['POST'])
def invoice_export():
    logging.info("welcome invoice export...")

    ### Update the config data
    payload = request.get_json()

    ### FileUtil
    fileUtil = FileUtil()
    fileUtil.start()

    ### TurboMain
    configUtil = current_app.config["configUtil"]
    invoiceMain = InvoiceMain(fileUtil, configUtil)

    resp = invoiceMain.exportInovice()
    return resp, 200
