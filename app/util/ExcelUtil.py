import pandas as pd
import logging
import os


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
        excel_writer.save()

        self.logger.info(f'Excel file "{fileName}" has been created and saved.')
