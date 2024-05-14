from datetime import datetime, timedelta
import pandas as pd
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
