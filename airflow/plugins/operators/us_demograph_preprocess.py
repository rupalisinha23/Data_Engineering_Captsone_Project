from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import logging
from airflow.contrib.hooks.aws_hook import AwsHook
import pandas as pd
import os


class USDemographPreprocessOperator(BaseOperator):
    """
    This class is to define the pre-processing steps for 
    us_cities_demographics data and puts them to pre_processed_csv folder.
    """

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 aws_credentials_id,
                 input_path,
                 output_path,
                 file_ext,
                 *args, **kwargs):

        super(USDemographPreprocessOperator, self).__init__(*args, **kwargs)
        self.aws_credentials_id = aws_credentials_id
        self.input_path = input_path
        self.output_path = output_path
        self.file_ext = file_ext

    def execute(self, context):
        logging.info('Reading AWS Credentials. ')
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        
        
        logging.info('Reading the US cities demograph data in csv format.')
        df = pd.read_csv(self.input_path, sep=';')
        
        logging.info('Removing spaces in header names.')
        df.columns = ['City', 'State', 'Median_Age', 'Male_Population', 'Female_Population', \
               'Total_Population', 'Number_of_Veterans', 'Foreign-born', \
               'Average_Household_Size', 'State_Code', 'Race', 'Count'] 
        
        logging.info('Dropping duplicate rows.')
        df.drop_duplicates(keep=False,inplace=True) 
        
        logging.info('Dropping NULL rows.')
        df = df.dropna(how='any',axis=0)
        
        # save pre-processed data to csv
        logging.info('Saving the pre-processed file to csv...')
        filename = os.path.basename(self.input_path)
        df.to_csv(os.path.join(self.output_path,filename), index=False)
        
        