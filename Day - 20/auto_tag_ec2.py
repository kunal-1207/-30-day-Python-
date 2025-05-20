# Day 20
# Challenge: Auto-tag untagged AWS EC2 instances with default tags.
# Focus: boto3 advanced use
# Example Hint: EC2 create_tags() method

import boto3
from botocore.exceptions import ClientError
import argparse

DEFAULT_TAGS = {
    "Environment": "Dev",
    "Owner": "DevOps",
    "AutoTagged": "True"
}

def get_instances(region):
    ec2 = boto3.client('ec2', region_name=region)
    try:
        paginator = ec2.get_paginator('describe_instances')
        response_iterator = paginator.paginate()
        instances = []
        for page in response_iterator:
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    instances.append(instance)
        return instances
    except ClientError as e:
        print(f"Error fetching EC2 instances: {e}")
        return []

def identify_untagged(instances):
    untagged_instances = []
    for instance in instances:
        instance_id = instance['InstanceId']
        current_tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
        missing_tags = {k: v for k, v in DEFAULT_TAGS.items() if k not in current_tags}
        if not current_tags or missing_tags:
            untagged_instances.append((instance_id, missing_tags))
    return untagged_instances

def apply_tags(region, untagged_instances, dry_run=False):
    ec2 = boto3.client('ec2', region_name=region)
    for instance_id, missing_tags in untagged_instances:
        if not missing_tags:
            continue  # nothing to tag
        tag_list = [{'Key': k, 'Value': v} for k, v in missing_tags.items()]
        try:
            if dry_run:
                print(f"[DRY-RUN] Would tag {instance_id} with: {missing_tags}")
            else:
                ec2.create_tags(Resources=[instance_id], Tags=tag_list)
                print(f"Tagged {instance_id} with: {missing_tags}")
        except ClientError as e:
            print(f"Error tagging {instance_id}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Auto-tag EC2 instances with default tags.")
    parser.add_argument('--region', required=True, help='AWS region (e.g., us-west-2)')
    parser.add_argument('--dry-run', action='store_true', help='Simulate tagging without applying changes')
    args = parser.parse_args()

    print(f"Scanning EC2 instances in region: {args.region}")
    instances = get_instances(args.region)
    untagged_instances = identify_untagged(instances)
    
    if not untagged_instances:
        print("All instances are fully tagged.")
        return

    print(f"Found {len(untagged_instances)} untagged or partially tagged instances.")
    apply_tags(args.region, untagged_instances, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
