from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (USDemographPreprocessOperator, AirportPreprocessOperator,
                              TemperaturePreprocessOperator, SASToCSVOperator,
                              SAS7ToParquet, TransferToS3Operator, DataQualityOperator)
from airflow.operators.subdag_operator import SubDagOperator
from subdags.load_data_subdag import load_data_subdag
from subdags.create_table_subdag import create_table_subdag
from subdags.drop_table_subdag import drop_table_subdag
from helpers import SqlQueries
from airflow.models import Variable

AWS_KEY = os.environ.get('AWS_KEY')
AWS_SECRET = os.environ.get('AWS_SECRET')


default_args = {
    'owner': 'udacity',
    'start_date': datetime(2020, 6, 12),
#     'end_date': datetime(2020, 6, 12),
    'email_on_retry': False,
    'retires': 3,
    'catchup': False,
    'retry_delay': timedelta(minutes=5),
    'depends_on_past': False,
    'wait_for_downstream': True
}


dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Data Engineering Capstone Project',
#           schedule_interval='@once'
          schedule_interval='0 7 * * *'
        )


# start operator
start_operator = DummyOperator(task_id='Begin_execution',
                               dag=dag)


# preprocess for US demographic data
us_demograph_preprocess = USDemographPreprocessOperator(
    task_id='process_us_demograph',
    dag=dag,
    aws_credentials_id='aws_credentials',
    input_path=Variable.get('us_cities_demograph'),
    output_path=Variable.get("pre_processed_csv"),
    file_ext="csv",
    provide_context=True
)


# preprocess for airport codes data
airport_preprocess = AirportPreprocessOperator(
    task_id='process_airport_code',
    dag=dag,
    aws_credentials_id='aws_credentials',
    input_path=Variable.get('airport_codes'),
    output_path=Variable.get('pre_processed_csv'),
    file_ext='csv',
    provide_context=True
)


# pre-process for temperature data.
temperature_preprocess = TemperaturePreprocessOperator(
    task_id='process_temperature',
    dag=dag,
    aws_credentials_id='aws_credentials',
    input_path=Variable.get('temperature'),
    output_path=Variable.get('pre_processed_csv'),
    file_ext='csv',
    provide_context=True
)


# sas to csv for label description file to make them into fact data in csv format
convert_sas_to_csv = SASToCSVOperator(
    task_id='sas_to_csv',
    dag=dag,
    input_path=Variable.get("sas_file"),
    output_path=Variable.get("pre_processed_csv"),
    provide_context=True
)


# sas7bdat to parquet conversion
convert_sas7bdat_to_parquet = SAS7ToParquet (
    task_id='sas7bdat_to_parquet',
    dag=dag,
    input_path=Variable.get("sas7bdat_file"),
    output_path=Variable.get("pre_processed_parquet"),
    provide_context=True
)


# transfer csv data to s3
transfer_to_s3_csv = TransferToS3Operator(
    task_id='transfer_to_s3_csv',
    dag=dag,
    aws_credentials_id="aws_credentials",
    input_path=Variable.get("pre_processed_csv"),
    bucket_name=Variable.get("s3_bucket"),
    file_ext="csv",
    provide_context=True
)


# transfer parquet to s3
transfer_to_s3_parquet = TransferToS3Operator(
    task_id='transfer_to_s3_parquet',
    dag=dag,
    aws_credentials_id="aws_credentials",
    input_path=Variable.get("pre_processed_parquet"),
    bucket_name=Variable.get("s3_bucket"),
    file_ext="parquet",
    provide_context=True
)


# drop all the tables if they already exist
drop_table_subdag = SubDagOperator(
    subdag=drop_table_subdag(
        parent_dag_name="udac_example_dag",
        task_id="drop_table",
        redshift_conn_id="redshift",
        start_date=datetime(2020, 6, 12)
    ),
    task_id="drop_table",
    dag=dag
)


# create tables
create_table_subdag = SubDagOperator(
    subdag=create_table_subdag(
        parent_dag_name="udac_example_dag",
        task_id="create_table",
        redshift_conn_id="redshift",
        start_date=datetime(2020, 6, 12)
    ),
    task_id="create_table",
    dag=dag
)


# load data from s3 to the tables in redshift
load_data_subdag_task = SubDagOperator(
    subdag=load_data_subdag(
        parent_dag_name="udac_example_dag",
        task_id="load_data_to_redshift",
        redshift_conn_id="redshift",
        start_date=datetime(2019, 1, 1)
    ),
    task_id="load_data_to_redshift",
    dag=dag
)


# data quality check--> 1. check for no rows returned; 2. check for 0 rows returned
run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tables=['us_cities_demographics', \
            'airport_codes', \
            'temperature', \
            'i94port', \
            'i94visa', \
            'i94mode', \
            'i94citres', \
            'i94addr', \
            'immigration'],
)


# end operator
end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)    


# define the connections of operators
start_operator >> us_demograph_preprocess
start_operator >> airport_preprocess
start_operator >> temperature_preprocess
start_operator >> convert_sas_to_csv
start_operator >> convert_sas7bdat_to_parquet

us_demograph_preprocess >> transfer_to_s3_csv
airport_preprocess >> transfer_to_s3_csv
temperature_preprocess >> transfer_to_s3_csv
convert_sas_to_csv >> transfer_to_s3_csv
convert_sas7bdat_to_parquet >> transfer_to_s3_parquet

transfer_to_s3_csv >> drop_table_subdag
transfer_to_s3_parquet >> drop_table_subdag

drop_table_subdag >> create_table_subdag

create_table_subdag >> load_data_subdag_task

load_data_subdag_task >> run_quality_checks

run_quality_checks >> end_operator

