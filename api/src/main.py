from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

# import getpass
import os
import logging 
from dotenv import load_dotenv

from flask_basicauth import BasicAuth
from flask_login import login_required, fresh_login_required

from api.ApiTurbo import apiTurbo
from api.ApiMisc import apiMisc
from api.ApiConfig import apiConfig
from api.ApiExcel import apiExcel
from api.ApiExcelPro import apiExcelPro
from api.ApiInvoice import apiInvoice
from api.ApiEnvizi import apiEnvizi
from api.ApiWebhook import apiWebhook
from api.ApiUtilityBill import apiUtilityBill


from util.ConfigUtil import ConfigUtil

#### Logging Configuration
logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s',
    handlers=[
        logging.StreamHandler(), #print to console
    ],
    level=logging.INFO
)

app = Flask(__name__)
CORS(app)

# auth = BasicAuth(app)

app.register_blueprint(apiTurbo)
app.register_blueprint(apiMisc)
app.register_blueprint(apiConfig)
app.register_blueprint(apiExcel)
app.register_blueprint(apiExcelPro)
app.register_blueprint(apiInvoice)
app.register_blueprint(apiEnvizi)
app.register_blueprint(apiWebhook)
app.register_blueprint(apiUtilityBill)

# app.config['STATIC_FOLDER'] = 'static'  # Tells Flask to use 'static' as the static folder name

@app.route('/')
# @auth.login_required
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

### Main method
def main():
    logging.info("main started .....")
    load_dotenv()

    # Configure basic authentication
    # app.config['BASIC_AUTH_USERNAME'] = os.getenv("APP_USERNAME", "admin")
    # app.config['BASIC_AUTH_PASSWORD'] = os.getenv("APP_PASSWORD", "admin")

    configUtil = ConfigUtil()
    app.config["configUtil"] = configUtil


    # Get all attributes of the module
    module_attributes = dir(ConfigUtil)
    # Print the list of attributes
    print(module_attributes)
    

    ### Run the app
    app.run(host ='0.0.0.0', port = 3001, debug = False)

if __name__ == '__main__':
    main()