import pandas as pd
import logging
import os
from datetime import datetime
from util.DateUtils import DateUtils


class ExcelUtil(object):

    def __init__(
        self
    ) -> None:
        self.init_config()

    def init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    def generateExcel(self, fileName, sheetName, myData):
        # Create a DataFrame from the data
        df = pd.DataFrame(myData)

        # Define the Excel writer
        excel_writer = pd.ExcelWriter(fileName, engine='xlsxwriter')

        # Convert the DataFrame to an Excel object and save it
        df.to_excel(excel_writer, sheet_name=sheetName, index=False)

        # Save the Excel file
        excel_writer.close()

        self.logger.info(f'Excel file "{fileName}" has been created and saved.')

    def getColumnValue(self, row, column_name):
        result = ""
        try:
            result = row[column_name]
            if pd.isna(result):
                result = ''  # Replace 'nan' with empty string
            elif isinstance(result, datetime):
                result = DateUtils.dateToString(result)
        except Exception as e:
            self.logger.info(f"Error in reading a column from {column_name} from the excel : {e}")
            result = ""
        return result
        
    def readColumnName(self, fileNameWithPath):

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(fileNameWithPath)

        # Get the column names (header)
        column_names = df.columns.tolist()

        return column_names


    def getExcelAsJsonArray(self, fileNameWithPath) : 
        # Convert DataFrame to JSON

        columnNames = self.readColumnName(fileNameWithPath)
        processed_data = []
        self.logger.info(f"columnNames -------> {columnNames} ")

        df = pd.read_excel(fileNameWithPath)
        for i, row in df.iterrows():
            processed_row = {}
            index=0
            for column in columnNames:
                self.logger.info(f"column -------> {column} ")

                column_value = self.getColumnValue(row, column)
                processed_row[column] = column_value

            self.logger.info(f"processed_row -------> {processed_row} ")

            # Append the processed row to the list
            processed_data.append(processed_row)
        
        return processed_data