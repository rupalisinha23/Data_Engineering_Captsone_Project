import boto3
import json
import aws_utils
import argparse
import configparser

if __name__=='__main__':
    
    # parse the needed configuration
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', type=str, help="type an action either of creating the cluster of deleting it")
    args = parser.parse_args()
    action = args.action
    
    if action == 'create':
        # create iam role and attach policy
        roleArn = aws_utils.create_iam()
        print('IAM role has been created successfully!')
        print('========================================')
        
        # create redshift cluster
        cluster_endpoint = aws_utils.create_redshift_cluster(roleArn)
        print('roleArn: ', roleArn)
        print('Cluster Endpoint: ', cluster_endpoint)
    
    elif action == 'delete':
        print('Deleting the cluster')
        aws_utils.delete_redshift_cluster()
