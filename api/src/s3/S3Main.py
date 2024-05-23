import boto3
from botocore.exceptions import NoCredentialsError
import os
from util.ConfigUtil import ConfigUtil
import logging

class S3Main(object):

    def __init__(
        self,
        configUtil: ConfigUtil,
    ) -> None:
        self.configUtil = configUtil
        self.logger = logging.getLogger(__name__)

    def pushFileToS3(self, fileNameWithPathToUpload, s3FileName):
        self.logger.info(f'-----------------------------------   S3Main pushFileToS3  Started -------------------------------------------')

        STOP_S3_PUSH = os.environ.get('STOP_S3_PUSH', "FALSE")
        
        if (STOP_S3_PUSH == "TRUE") : 
            self.logger.info(f'STOP_S3_PUSH flag is enabled, so the file is not pushed to S3')
        else:
            # Initialize a session using your AWS credentials
            s3 = boto3.client('s3', aws_access_key_id=self.configUtil.ENVIZI_S3_AWS_ACCESS_KEY, aws_secret_access_key=self.configUtil.ENVIZI_S3_AWS_SECRET_KEY)

            s3FileName = self.configUtil.ENVIZI_S3_AWS_FOLDER_NAME + "/" + s3FileName
            try:
                # Upload the file to the specified S3 bucket
                s3.upload_file(fileNameWithPathToUpload, self.configUtil.ENVIZI_S3_AWS_BUCKET_NAME, s3FileName)
                self.logger.info(f'{fileNameWithPathToUpload} is uploaded to {self.configUtil.ENVIZI_S3_AWS_BUCKET_NAME}  : {s3FileName}')
            except Exception as e:
                self.logger.error(f' Error in pushFileToS3 : {e} ')

        self.logger.info(f'-----------------------------------   S3Main pushFileToS3  completed -------------------------------------------')


