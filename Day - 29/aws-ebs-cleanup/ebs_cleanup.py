import boto3
from datetime import datetime, timezone, timedelta
import logging
import socket
import urllib3

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_internet_connection():
    """Check if we have internet connectivity"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

def cleanup_old_untagged_volumes(region_name='us-east-1', days_threshold=30, dry_run=True):
    """
    Identify and delete old, untagged EBS volumes in AWS.
    
    Args:
        region_name (str): AWS region to operate in
        days_threshold (int): Number of days a volume must be older than to be considered for deletion
        dry_run (bool): If True, only log what would be deleted without actually deleting
    """
    # Check internet connection first
    if not check_internet_connection():
        logger.error("No internet connection available")
        return

    try:
        # Initialize EC2 client with longer timeout
        config = boto3.session.Config(
            connect_timeout=10,
            read_timeout=30,
            retries={'max_attempts': 3}
        )
        ec2 = boto3.client('ec2', region_name=region_name, config=config)
        
        # Test connection by getting caller identity
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        logger.info(f"Connected to AWS as: {identity['Arn']}")
        
        # Calculate cutoff time (using timezone-aware datetime)
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=days_threshold)
        
        # Get all volumes with pagination
        paginator = ec2.get_paginator('describe_volumes')
        volume_page_iterator = paginator.paginate()
        
        deleted_count = 0
        skipped_count = 0
        
        for page in volume_page_iterator:
            for volume in page['Volumes']:
                volume_id = volume['VolumeId']
                create_time = volume['CreateTime']
                
                # Check if volume is in use
                if volume['State'] != 'available':
                    logger.debug(f"Skipping volume {volume_id} - not in 'available' state")
                    skipped_count += 1
                    continue
                
                # Check if volume is older than threshold
                if create_time > cutoff_time:
                    logger.debug(f"Skipping volume {volume_id} - created recently ({create_time})")
                    skipped_count += 1
                    continue
                
                # Check for tags - skip if any tags exist
                if 'Tags' in volume and volume['Tags']:
                    logger.debug(f"Skipping volume {volume_id} - has tags")
                    skipped_count += 1
                    continue
                
                # If we get here, volume is eligible for deletion
                logger.info(f"Found volume to delete: {volume_id} (created {create_time}, untagged)")
                
                if not dry_run:
                    try:
                        ec2.delete_volume(VolumeId=volume_id)
                        logger.info(f"Successfully deleted volume {volume_id}")
                        deleted_count += 1
                    except Exception as e:
                        logger.error(f"Failed to delete volume {volume_id}: {str(e)}")
                else:
                    logger.info(f"DRY RUN: Would delete volume {volume_id}")
                    deleted_count += 1
        
        logger.info(f"Cleanup complete. {deleted_count} volumes {'would be' if dry_run else 'were'} deleted. {skipped_count} volumes were skipped.")
    
    except urllib3.exceptions.NameResolutionError:
        logger.error(f"DNS resolution failed for region {region_name}. Please check:")
        logger.error("1. Your internet connection")
        logger.error("2. If the region name is correct (current: %s)", region_name)
        logger.error("3. Try a different region like 'us-east-1'")
    except boto3.exceptions.Boto3Error as e:
        logger.error(f"AWS API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    # Example usage - modify parameters as needed
    cleanup_old_untagged_volumes(
        region_name='ap-south-1',  # Try 'us-east-1' if this fails
        days_threshold=30,
        dry_run=True  # Keep as True until you verify it works
    )
