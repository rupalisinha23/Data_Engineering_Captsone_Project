from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
# from airflow import sql_statements
from helpers import SqlQueries


def create_table_subdag(parent_dag_name,
                          task_id,
                          redshift_conn_id,
                          *args, **kwargs):
    dag = DAG(
            f"{parent_dag_name}.{task_id}",
        **kwargs)
    
    create_us_demograph_table = PostgresOperator(
        task_id="create_us_demograph_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.CREATE_US_DEMOGRAPH_TABLE_SQL)
    
    create_airport_codes_table = PostgresOperator(
        task_id="create_airport_codes_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.CREATE_AIRPORT_CODES_TABLE_SQL)
    
    create_global_temperature_table = PostgresOperator(
        task_id="create_global_temperature_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.CREATE_GLOBAL_TEMPERATURE_TABLE_SQL)
    
    create_i94port_table = PostgresOperator(
        task_id="create_i94port_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.CREATE_I94PORT_TABLE_SQL)
    
    create_i94visa_table = PostgresOperator(
        task_id="create_i94visa_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.CREATE_I94VISA_TABLE_SQL)
    
    create_i94mode_table = PostgresOperator(
        task_id="create_i94mode_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.CREATE_I94MODE_TABLE_SQL)
    
    create_i94citres_table = PostgresOperator(
        task_id="create_i94citres_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.CREATE_I94CITRES_TABLE_SQL)
    
    create_i94addr_table = PostgresOperator(
        task_id="create_i94addr_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.CREATE_I94ADDR_TABLE_SQL)
    
    create_i94immigration_table = PostgresOperator(
        task_id="create_i94immigration_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.CREATE_IMMIGRATION_TABLE_SQL)


    create_us_demograph_table
    create_airport_codes_table
    create_global_temperature_table
    create_i94port_table
    create_i94visa_table
    create_i94mode_table
    create_i94citres_table
    create_i94addr_table
    create_i94immigration_table
    
    return dag