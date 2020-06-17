import configparser

config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

# read the configuration parameters
# amazon aws
KEY = config.get('AWS', 'key')
SECRET = config.get('AWS', 'secret')

# Redshift
DWH_DB = config.get('DWH', 'DWH_DB')
DWH_DB_USER = config.get('DWH', 'DWH_DB_USER')
DWH_DB_PASSWORD = config.get('DWH', 'DWH_DB_PASSWORD')
DWH_PORT = config.get('DWH', 'DWH_PORT')
DWH_CLUSTER_TYPE = config.get('DWH', 'DWH_CLUSTER_TYPE')
DWH_NUM_NODES = config.get('DWH', 'DWH_NUM_NODES')
DWH_NODE_TYPE = config.get('DWH', 'DWH_NODE_TYPE')
DWH_IAM_ROLE_NAME = config.get('DWH', 'DWH_IAM_ROLE_NAME')
DWH_CLUSTER_IDENTIFIER = config.get('DWH', 'DWH_CLUSTER_IDENTIFIER')
DWH_SCHEMA = config.get('DWH', 'DWH_SCHEMA')
DWH_REGION = config.get('DWH', 'DWH_REGION')
