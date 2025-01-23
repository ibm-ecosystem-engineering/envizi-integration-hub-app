from datetime import datetime, timedelta
import logging
import os, json

### Static methods
class JsonUtil :
    
    logger = logging.getLogger('JsonUtil')
    logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    @staticmethod
    # Function to find an element based on the value of a key
    def findElement(jsonArray, key, value):
        for item in jsonArray:
            if item.get(key) == value:
                return item
        return None  # Return None if element not found

    @staticmethod
    def loadJsonFileContent(fileName):
        # JsonUtil.logger.debug("loadJsonFileContent  ... :  " + fileName)
        data = {}
        try:
            with open(fileName, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            JsonUtil.logger.error(f"The file '{fileName}' does not exist.")
        except json.JSONDecodeError:
            JsonUtil.logger.error(f"The file '{fileName}' is not valid JSON.")

        return data
    
    @staticmethod
    def saveJsonFileContent(fileName, json_data):
        # JsonUtil.logger.debug("saveJsonFileContent  ... :  " + fileName)
        try:
            with open(fileName, 'w') as file:
                json.dump(json_data, file, indent=4)  # Write the dictionary back to the file with formatting
        except Exception:
            JsonUtil.logger.error(f"The file '{fileName}' is not saved")

        return json_data    
    
    @staticmethod
    def loadJsonArrayFileContent(fileName):
        # JsonUtil.logger.debug("loadJsonArrayFileContent  ... :  " + fileName)
        data = []
        try:
            with open(fileName, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            JsonUtil.logger.error(f"The file '{fileName}' does not exist.")
        except json.JSONDecodeError:
            JsonUtil.logger.error(f"The file '{fileName}' is not valid JSON.")

        return data

    @staticmethod
    def add_record_to_json_file(fileName, new_record):
        JsonUtil.logger.debug("add_record_to_json_file  ... :  " + fileName)
        
        ### Load existing file
        data = JsonUtil.loadJsonArrayFileContent(fileName)

        ### Append a new record
        data.append(new_record)

        ### Save the file
        JsonUtil.saveJsonFileContent(fileName, data)

        return data
    
    @staticmethod
    def update_record_to_json_file(fileName, find_key, find_value, key1, value1, key2, value2):
        # JsonUtil.logger.debug("update_record_to_json_file  ... :  " + fileName)
        
        ### Load existing file
        data = JsonUtil.loadJsonArrayFileContent(fileName)

        for item in data:
            if item.get(find_key) == find_value:
                item[key1] = value1
                item[key2] = value2
                break

        ### Save the file
        JsonUtil.saveJsonFileContent(fileName, data)

        return data 