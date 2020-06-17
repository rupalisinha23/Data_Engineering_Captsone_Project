import boto3
import json
from config import *
from clients import *
from botocore.exceptions import ClientError
import sys
import time

def animate():
    chars = r"|/-\|"
    for char in chars:
        sys.stdout.write('\r' + 'Please wait ...' + char)
        time.sleep(.1)
        sys.stdout.flush()
        
        
def create_iam():
    """
    This function creates the client to iam, creates the role and attaches the policy.
    :parm None
    :return: roleArn
    """
    
    # create the role
    try:
        print("Creating a new IAM Role") 
        dwhRole = iam.create_role(
            Path='/',
            RoleName=DWH_IAM_ROLE_NAME,
            Description = "Allows Redshift clusters to call AWS services on your behalf.",
            AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                   'Effect': 'Allow',
                   'Principal': {'Service': 'redshift.amazonaws.com'}}],
                 'Version': '2012-10-17'}))   
    except Exception as e:
        print(e)


    # attach the policy
    print("Attaching Policy")
    iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME,
                           PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                          )['ResponseMetadata']['HTTPStatusCode']

    # save the iam role arn
    print("Get the IAM role ARN")
    roleArn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']

    return roleArn


def create_redshift_cluster(roleArn):
    """
    This function creates the redshift cluster.
    :parm roleArn
    :return: 
    """
    try:
        response = redshift.create_cluster(        
            #HW
            ClusterType=DWH_CLUSTER_TYPE,
            NodeType=DWH_NODE_TYPE,
            NumberOfNodes=int(DWH_NUM_NODES),

            #Identifiers & Credentials
            DBName=DWH_DB,
            ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
            MasterUsername=DWH_DB_USER,
            MasterUserPassword=DWH_DB_PASSWORD,

            #Roles (for s3 access)
            IamRoles=[roleArn]  
        )
    except Exception as e:
        print(e)
    
    print('Cluster is being created!')
    while redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]['ClusterStatus'] \
                                                                                                != 'available':
        animate()

    print("Cluster is created successfully!")
    
    
    # open an existing TCP port to access the cluster
    try:
        vpc = ec2.Vpc(id=redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)\
                                    ['Clusters'][0]['VpcId'])
        defaultSg = list(vpc.security_groups.all())[0]
        print(defaultSg)
        defaultSg.authorize_ingress(
            GroupName=defaultSg.group_name,
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(DWH_PORT),
            ToPort=int(DWH_PORT)
        )
        print('TCP inbound port is now opened.')
    except Exception as e:
        print(e)
    
    return redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)\
                                    ['Clusters'][0]['Endpoint']['Address']


def delete_redshift_cluster():
    """
    This function deletes the cluster.
    :parm
    :return:
    """
    try:
        redshift.delete_cluster(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
                                SkipFinalClusterSnapshot=True)
    except ClientError as e:
        print(e)

    try:   
        print("Cluster is being deleted.")
        while redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)\
                                            ['Clusters'][0]['ClusterStatus'] == 'deleting':
            animate()
    except:
        print('Cluster has been successfully deleted!')

    
    # detach policy
    iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME, PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
    iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
    print('Policy is detached and role is deleted.')
    return None