# Day 21
# Challenge: Script to reboot EC2 instances based on CPU thresholds.
# Focus: boto3, monitoring
# Example Hint: Use CloudWatch metrics API

import boto3
import datetime
import logging
import argparse
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Constants
CPU_THRESHOLD = 90.0  # CPU utilization threshold in percent
PERIOD_MINUTES = 5    # Time period to check utilization
NAMESPACE = 'AWS/EC2'
METRIC_NAME = 'CPUUtilization'
STATISTIC = 'Average'
REGION = 'us-east-1'  # Change to your desired region

def get_running_instances(ec2):
    """Return a list of running EC2 instance IDs."""
    try:
        response = ec2.describe_instances(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
        instance_ids = [
            instance['InstanceId']
            for reservation in response['Reservations']
            for instance in reservation['Instances']
        ]
        logging.info(f"Found {len(instance_ids)} running instance(s).")
        return instance_ids
    except ClientError as e:
        logging.error(f"Error fetching EC2 instances: {e}")
        return []

def get_cpu_utilization(cloudwatch, instance_id):
    """Get average CPU utilization for an instance over the last PERIOD_MINUTES."""
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(minutes=PERIOD_MINUTES)

    try:
        response = cloudwatch.get_metric_statistics(
            Namespace=NAMESPACE,
            MetricName=METRIC_NAME,
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=PERIOD_MINUTES * 60,
            Statistics=[STATISTIC]
        )
        datapoints = response.get('Datapoints', [])
        if not datapoints:
            logging.warning(f"No CPU data for instance {instance_id}.")
            return 0.0
        avg_cpu = datapoints[0][STATISTIC]
        logging.info(f"Instance {instance_id} average CPU: {avg_cpu:.2f}%")
        return avg_cpu
    except ClientError as e:
        logging.error(f"Error fetching CPU data for {instance_id}: {e}")
        return 0.0

def reboot_instance(ec2, instance_id, dry_run=True):
    """Attempt to reboot an EC2 instance with dry-run option."""
    try:
        ec2.reboot_instances(InstanceIds=[instance_id], DryRun=dry_run)
        if dry_run:
            logging.info(f"Dry-run successful for rebooting instance {instance_id}.")
        else:
            logging.info(f"Instance {instance_id} rebooted.")
    except ClientError as e:
        if 'DryRunOperation' in str(e):
            logging.info(f"Dry-run confirmed. Instance {instance_id} can be rebooted.")
        elif 'UnauthorizedOperation' in str(e):
            logging.error(f"Unauthorized to reboot instance {instance_id}: {e}")
        else:
            logging.error(f"Error rebooting instance {instance_id}: {e}")

def main(dry_run):
    ec2 = boto3.client('ec2', region_name=REGION)
    cloudwatch = boto3.client('cloudwatch', region_name=REGION)

    instance_ids = get_running_instances(ec2)
    for instance_id in instance_ids:
        cpu = get_cpu_utilization(cloudwatch, instance_id)
        if cpu > CPU_THRESHOLD:
            logging.warning(f"Instance {instance_id} exceeds CPU threshold: {cpu:.2f}%")
            reboot_instance(ec2, instance_id, dry_run=dry_run)
        else:
            logging.info(f"Instance {instance_id} is within CPU limits.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Reboot EC2 instances with high CPU usage.")
    parser.add_argument('--dry-run', action='store_true', help="Perform a dry run without rebooting instances.")
    args = parser.parse_args()

    main(dry_run=args.dry_run)
