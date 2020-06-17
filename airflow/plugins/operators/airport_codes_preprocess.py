from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import logging
from airflow.contrib.hooks.aws_hook import AwsHook
import pandas as pd
import os


class AirportPreprocessOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 aws_credentials_id,
                 input_path,
                 output_path,
                 file_ext,
                 *args, **kwargs):

        super(AirportPreprocessOperator, self).__init__(*args, **kwargs)
        self.aws_credentials_id = aws_credentials_id
        self.input_path = input_path
        self.output_path = output_path
        self.file_ext = file_ext

    def execute(self, context):
        logging.info('Reading AWS Credentials. ')
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        
        
        logging.info('Reading the US cities demograph data in csv format.')
        df = pd.read_csv(self.input_path)
  
        
        # save pre-processed data to csv
        logging.info('Saving the pre-processed file to csv...')
        filename = os.path.basename(self.input_path)
        df.to_csv(os.path.join(self.output_path,filename), index=False)
        
        