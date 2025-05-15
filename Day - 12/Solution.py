# Day 12
# Challenge: Fetch EC2 instance statuses using Boto3.
# Focus: AWS SDK (boto3), API interaction
# Example Hint: Install boto3 using pip

import logging
import boto3

def get_ec2_instance_statuses(
    region_name='ap-south-1',
    aws_access_key_id=None,
    aws_secret_access_key=None,
    aws_session_token=None
):
    ec2 = boto3.client(
        'ec2',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token
    )
    try:
        paginator = ec2.get_paginator('describe_instance_status')
        instance_statuses = []
        for page in paginator.paginate(IncludeAllInstances=True):
            for status in page.get('InstanceStatuses', []):
                if all(k in status for k in ['InstanceId', 'InstanceState', 'InstanceStatus', 'SystemStatus']):
                    instance_info = {
                        'InstanceId': status['InstanceId'],
                        'InstanceState': status['InstanceState'].get('Name'),
                        'InstanceStatus': status['InstanceStatus'].get('Status'),
                        'SystemStatus': status['SystemStatus'].get('Status')
                    }
                    instance_statuses.append(instance_info)
                else:
                    missing_keys = [k for k in ['InstanceId', 'InstanceState', 'InstanceStatus', 'SystemStatus'] if k not in status]
                    logging.warning(f"Missing expected keys in status: {missing_keys}")
        return instance_statuses
    except Exception as e:
        logging.error(f"Failed to describe instance status: {e}")
        return []

def list_all_ec2_instances(region_name='ap-south-1'):
    ec2 = boto3.client('ec2', region_name=region_name)
    try:
        response = ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                print(f"InstanceId: {instance_id}, State: {state}")
                instances.append({'InstanceId': instance_id, 'State': state})
        if not instances:
            print("No EC2 instances found in this region.")
        return instances
    except Exception as e:
        logging.error(f"Failed to list EC2 instances: {e}")
        return []

if __name__ == "__main__":
    print("Checking all EC2 instances in ap-south-1:")
    list_all_ec2_instances()
    print("\nChecking instance statuses:")
    statuses = get_ec2_instance_statuses()
    print(statuses)
