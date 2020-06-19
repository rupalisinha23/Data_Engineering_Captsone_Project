from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
    This class is to perform the data quality checks on the redhsift tables.
    """

    ui_color = '#FFC0CB' 

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 tables,
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.tables = tables

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        for current_table in self.tables:
            records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {current_table}")
            
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError (f"Data quality check failed. {current_table} returned no results.")
                
            num_records = records[0][0]
            if num_records < 1:
                raise ValueError (f"Data quality check failed. {current_table} returned 0 rows.")
            
            self.log.info(f"Data quality on table {current_table} check passed with {records[0][0]} records.")