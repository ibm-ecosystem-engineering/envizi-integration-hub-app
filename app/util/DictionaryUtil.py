from datetime import datetime, timedelta
import logging
import os

### Static methods
class DictionaryUtil :

    logger = logging.getLogger('DictionaryUtil')
    logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    @staticmethod
    def getValue_key1(dicObject, key1, defaultValue):
        result = defaultValue
        try:
            if key1 in dicObject :
                result = dicObject[key1]
        except Exception as e:
            DictionaryUtil.logger.debug (f' Error in getValue_key1 : {e} ')
        return result
    

    @staticmethod
    def getValue_key2_index(dicObject, key1, key2, index, defaultValue):
        result = defaultValue
        try:
            dicObject = dicObject[0]
            if key1 in dicObject and key2 in dicObject[key1] and len(dicObject[key1][key2] > index) :
                result = dicObject[key1][key2][0]
        except Exception as e:
            DictionaryUtil.logger.debug (f' Error in getValue_key2_index : {e} ')
        return result
    
    @staticmethod
    def getValue_key4(dicObject, key1, key2, key3, key4, defaultValue):
        result = defaultValue
        try:
            # dicObject = dicObject[0]
            result = dicObject [key1][key2][key3][key4] 
        except Exception as e:
            DictionaryUtil.logger.debug (f' Error in getValue_key4 : {e} ')
        return result
    
    @staticmethod
    def getSum_key1_subkey2(dicObject, key1, subKey1, subKey2, defaultValue):
        result = defaultValue
        sum_values_total = 0
        try:
            dicObject = dicObject[0]
            rows = dicObject[key1]
            for row in rows: 
                sum_values_total = sum_values_total + row[subKey1][subKey2]
            result = sum_values_total
        except Exception as e:
            DictionaryUtil.logger.debug (f' Error in getSum_key1_subkey2 : {e} ')
        return result
    
    @staticmethod
    def getCount_key1(dicObject, key1):
        result = 0
        count = 0
        try:
            dicObject = dicObject[0]
            rows = dicObject[key1]
            result = len(rows)
        except Exception as e:
            DictionaryUtil.logger.debug (f' Error in getCount_key1 : {e} ')

        return result