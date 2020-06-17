from airflow import DAG
from airflow.operators import StageToRedshiftOperator
from helpers import SqlQueries
from airflow.models import Variable
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
import logging
import boto3
from airflow.contrib.hooks.aws_hook import AwsHook


def load_data_subdag(
        parent_dag_name,
        task_id,
        redshift_conn_id,
        *args, **kwargs):
    """
    A python function with arguments, which creates a dag
    :param parent_dag_name: imp ({parent_dag_name}.{task_id})
    :param task_id: imp {task_id}
    :param redshift_conn_id: {any connection id}
    :param args: {verbose}
    :param kwargs: {verbose and context variables}
    :return:
    """
    dag = DAG(
        f"{parent_dag_name}.{task_id}",
        **kwargs
    )

    copy_port_data = StageToRedshiftOperator(
        task_id='copy_i94port',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        file='i94port.csv',
        delimiter=',',
        table='i94port',
        s3_bucket=Variable.get("s3_bucket"),
        s3_key="csv",
        sql_stmt=SqlQueries.COPY_CSV_DATA,
        provide_context=True)

    copy_visa_data = StageToRedshiftOperator(
        task_id='copy_i94visa',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        file='i94visa.csv',
        delimiter=',',
        table='i94visa',
        s3_bucket=Variable.get("s3_bucket"),
        s3_key="csv",
        sql_stmt=SqlQueries.COPY_CSV_DATA,
        provide_context=True)

    copy_mode_data = StageToRedshiftOperator(
        task_id='copy_i94mode',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        file='i94mode.csv',
        delimiter=',',
        table='i94mode',
        s3_bucket=Variable.get("s3_bucket"),
        s3_key="csv",
        sql_stmt=SqlQueries.COPY_CSV_DATA,
        provide_context=True)

    copy_citres_data = StageToRedshiftOperator(
        task_id='copy_i94citres',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        file='i94cit&i94res.csv',
        delimiter=',',
        table='i94citres',
        s3_bucket=Variable.get("s3_bucket"),
        s3_key="csv",
        sql_stmt=SqlQueries.COPY_CSV_DATA,
        provide_context=True)

    copy_addr_data = StageToRedshiftOperator(
        task_id='copy_i94addr',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        file='i94addr.csv',
        delimiter=',',
        table='i94addr',
        s3_bucket=Variable.get("s3_bucket"),
        s3_key="csv",
        sql_stmt=SqlQueries.COPY_CSV_DATA,
        provide_context=True)

    copy_us_cities_demographics = StageToRedshiftOperator(
        task_id='copy_us_cities_demographics',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        file='us-cities-demographics.csv',
        delimiter=',',
        table='us_cities_demographics',
        s3_bucket=Variable.get("s3_bucket"),
        s3_key="csv",
        sql_stmt=SqlQueries.COPY_CSV_DATA,
        provide_context=True)
    
    copy_global_temperature_data = StageToRedshiftOperator(
        task_id='copy_global_temperature_data',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        file='GlobalLandTemperaturesByCity.csv',
        delimiter=',',
        table='temperature',
        s3_bucket=Variable.get("s3_bucket"),
        s3_key="csv",
        sql_stmt=SqlQueries.COPY_CSV_DATA,
        provide_context=True)

    copy_airport_codes = StageToRedshiftOperator(
        task_id='copy_airport_codes',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        file='airport-codes_csv.csv',
        delimiter=',',
        table='airport_codes',
        s3_bucket=Variable.get("s3_bucket"),
        s3_key="csv",
        sql_stmt=SqlQueries.COPY_CSV_DATA,
        provide_context=True)

    def parquet_to_redshift(table, s3_bucket, s3_key, iam_role,
                            sql_stmt, redshift_conn_id, **kwargs):
        """
        This function reads parquet files and copies them to redshift
        schema.db
        :param table:
        :param s3_bucket:
        :param s3_key:
        :param iam_role:
        :param sql_stmt:
        :param redshift_conn_id:
        :param kwargs:
        :return:
        """
        redshift = PostgresHook(postgres_conn_id=redshift_conn_id)
        logging.info("Copying data from S3 to Redshift")
        s3_path = "s3://{}/{}".format(s3_bucket, s3_key)
        formatted_sql = sql_stmt.format(
            table,
            s3_path,
            iam_role
        )
        redshift.run(formatted_sql)
        aws_hook = AwsHook("aws_credentials")
        credentials = aws_hook.get_credentials()
        client = boto3.client('s3',
                              aws_access_key_id=credentials.access_key,
                              aws_secret_access_key=credentials.secret_key)
        objects_to_delete = client.list_objects(
            Bucket=Variable.get("s3_bucket"), Prefix="parquet")
        delete_keys = {'Objects': []}
        delete_keys['Objects'] = [{'Key': k} for k in
                                  [obj['Key'] for obj in
                                   objects_to_delete.get('Contents',
                                                         [])]]
        client.delete_objects(Bucket=Variable.get("s3_bucket"),
                              Delete=delete_keys)

    copy_immigration_data = PythonOperator(
        task_id='copy_immigration_data',
        python_callable=parquet_to_redshift,  # changed
        provide_context=True,
        op_kwargs={'table': "immigration",
                   's3_bucket': Variable.get("s3_bucket"),
                   's3_key': 'parquet',
                   'iam_role': Variable.get('iam_role'),
                   'sql_stmt': SqlQueries.COPY_PARQUET_DATA,
                   'redshift_conn_id': 'redshift'},
        dag=dag
    )

    
    copy_port_data
    copy_visa_data
    copy_mode_data
    copy_citres_data
    copy_addr_data
    copy_us_cities_demographics
    copy_airport_codes
    copy_global_temperature_data
    copy_immigration_data

    return dag