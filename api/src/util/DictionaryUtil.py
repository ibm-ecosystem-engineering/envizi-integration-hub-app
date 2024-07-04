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
            # DictionaryUtil.logger.debug (f' Error in getValue_key1 : {e} ')
           result = defaultValue

        return result
    
    @staticmethod
    def getValue_key2(dicObject, key1, key2, defaultValue):
        result = defaultValue
        try:
            if key1 in dicObject and key2 in dicObject[key1] :
                result = dicObject[key1][key2]
        except Exception as e:
            # DictionaryUtil.logger.debug (f' Error in getValue_key2 : {e} ')
            result = defaultValue

        return result

    @staticmethod
    def getValue_key2_index(dicObject, key1, key2, index, defaultValue):
        result = defaultValue
        try:
            dicObject = dicObject[0]
            if key1 in dicObject and key2 in dicObject[key1] and len(dicObject[key1][key2] > index) :
                result = dicObject[key1][key2][0]
        except Exception as e:
            # DictionaryUtil.logger.debug (f' Error in getValue_key2_index : {e} ')
            result = defaultValue
        return result
    
    @staticmethod
    def getValue_key4(dicObject, key1, key2, key3, key4, defaultValue):
        result = defaultValue
        try:
            # dicObject = dicObject[0]
            result = dicObject [key1][key2][key3][key4] 
        except Exception as e:
            # DictionaryUtil.logger.debug (f' Error in getValue_key4 : {e} ')
            result = defaultValue
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
            # DictionaryUtil.logger.debug (f' Error in getSum_key1_subkey2 : {e} ')
            result = defaultValue

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
            # DictionaryUtil.logger.debug (f' Error in getCount_key1 : {e} ')
            result = 0

        return result
    
    @staticmethod
    def getStringOrFirstIndex(var):
        if isinstance(var, str):  # Check if the variable is a string
            return var  # Return the string as it is
        elif isinstance(var, list) and var:  # Check if the variable is a non-empty list
            return var[0]  # Return the first element of the list
        else:
            return None  # Return None if the variable is not a string or an empty list
        
    @staticmethod
    def geListAsString(var):
        if isinstance(var, str):  # Check if the variable is a string
            return var  # Return the string as it is
        elif isinstance(var, list) and var:  # Check if the variable is a non-empty list
            return ' '.join(var)  # Return the first element of the list
        else:
            return None  # Return None if the variable is not a string or an empty list

    @staticmethod
    def findValue (my_dict, text_expression) :
        result = None
        try:
            value = my_dict
            parts = text_expression.split('.')
            for part in parts:
                if '[' in part :
                    key = part.split('[')[0]
                    indice = part.split('[')[1].rstrip(']')
            
                    value = value[key][int(indice)]
                else :
                    value = value[part]
                result = value
        except Exception as e:
            # DictionaryUtil.logger.debug (f' Error in findValue : {e} ')
            result = None

        DictionaryUtil.logger.debug (f' DictionaryUtil findValue expression : {text_expression} ')
        DictionaryUtil.logger.debug (f' DictionaryUtil findValue value : {result} ')

        return result
    

    @staticmethod
    def appendIfDuplicate (dicObject, key, value) :
        result = True
        try:
            DictionaryUtil.logger.debug (f' appendIfDuplicate : key -> {key} : value : {value} ')

            if key in dicObject :
                result = dicObject[key]
                value = str(value) + "," + str(result)
                DictionaryUtil.logger.debug (f' appendIfDuplicate : found................ ....key -> {key} : value : {value} ')
            dicObject[key] = str(value)
        except Exception as e:
            DictionaryUtil.logger.debug (f' Error in appendIfDuplicate : {e} ')
            result = False

        return result