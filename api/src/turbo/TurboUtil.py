from datetime import datetime, timedelta
import logging
import os

from util.DictionaryUtil import DictionaryUtil

class TurboUtil :

    logger = logging.getLogger('TurboUtil')
    logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    @staticmethod
    def findEnergyConsumption(entitiesJson):
        result = 0
        try:
            sum = DictionaryUtil.getSum_key1_subkey2(entitiesJson, "statistics", "values", "total", 0)
            count = DictionaryUtil.getCount_key1(entitiesJson, "statistics")
            count = 144 if count == 1 else 6
            result = round((count * sum) / 1000, 4)
        except Exception as e:
            TurboUtil.logger.error(f' Error in findEnergyConsumption : {e} ')
        return result

    @staticmethod
    def findEnergyToHostIntensity(energyConsumption, activeHostCount):
        result = 0
        try:
            result = round(energyConsumption/activeHostCount, 4)
        except Exception as e:
            TurboUtil.logger.error(f' Error in findEnergyToHostIntensity : {e} ')
        return result

    @staticmethod
    def findVMToHostDensity(vMCount, activeHostCount):
        result = 0
        try:
            result = round(vMCount/activeHostCount, 4)
        except Exception as e:
            TurboUtil.logger.error(f' Error in findVMToHostDensity : {e} ')
        return result

