from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
# from airflow import sql_statements
from helpers import SqlQueries


def drop_table_subdag(parent_dag_name,
                          task_id,
                          redshift_conn_id,
                          *args, **kwargs):
    """
    This function is to drop the tables if they already exist in redshift.
    """
    dag = DAG(
            f"{parent_dag_name}.{task_id}",
        **kwargs)
    
    drop_us_demograph_table = PostgresOperator(
        task_id="drop_us_demograph_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.DROP_US_DEMOGRAPH_TABLE_SQL)
    
    drop_airport_codes_table = PostgresOperator(
        task_id="drop_airport_codes_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.DROP_AIRPORT_CODES_TABLE_SQL)
    
    drop_global_temperature_table = PostgresOperator(
        task_id="drop_global_temperature_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.DROP_GLOBAL_TEMPERATURE_TABLE_SQL)
    
    drop_i94port_table = PostgresOperator(
        task_id="drop_i94port_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.DROP_I94PORT_TABLE_SQL)
    
    drop_i94visa_table = PostgresOperator(
        task_id="drop_i94visa_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.DROP_I94VISA_TABLE_SQL)
    
    drop_i94mode_table = PostgresOperator(
        task_id="drop_i94mode_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.DROP_I94MODE_TABLE_SQL)
    
    drop_i94citres_table = PostgresOperator(
        task_id="drop_i94citres_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.DROP_I94CITRES_TABLE_SQL)
    
    drop_i94addr_table = PostgresOperator(
        task_id="drop_i94addr_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.DROP_I94ADDR_TABLE_SQL)
    
    drop_i94immigration_table = PostgresOperator(
        task_id="drop_i94immigration_table",
        dag=dag,
        postgres_conn_id="redshift",
        sql=SqlQueries.DROP_IMMIGRATION_TABLE_SQL)


    drop_us_demograph_table
    drop_airport_codes_table
    drop_global_temperature_table
    drop_i94port_table
    drop_i94visa_table
    drop_i94mode_table
    drop_i94citres_table
    drop_i94addr_table
    drop_i94immigration_table
    
    return dag