# Challenge: Poll an S3 bucket and auto-sync new files locally.
# Focus: boto3, file sync
# Example Hints: boto3, file sync

import boto3
import os
import time
import logging
from datetime import datetime
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class S3Sync:
    def __init__(self, bucket_name, local_dir, poll_interval=60):
        self.bucket_name = bucket_name
        self.local_dir = local_dir
        self.poll_interval = poll_interval
        
        try:
            # Initialize S3 client with ap-south-1 region
            self.s3 = boto3.client('s3', region_name='ap-south-1')
            
            # Verify bucket exists
            self.s3.head_bucket(Bucket=bucket_name)
            logger.info(f"Successfully connected to bucket: {bucket_name}")
            
            # Ensure local directory exists
            os.makedirs(local_dir, exist_ok=True)
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.error(f"Bucket '{bucket_name}' not found")
            elif error_code == '403':
                logger.error(f"Access denied to bucket '{bucket_name}'")
            else:
                logger.error(f"AWS error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            raise

    def sync_files(self):
        """Perform one sync operation"""
        try:
            # List all objects in the bucket
            paginator = self.s3.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=self.bucket_name):
                if 'Contents' not in page:
                    continue
                    
                for obj in page['Contents']:
                    key = obj['Key']
                    if key.endswith('/'):  # Skip directories
                        continue
                        
                    local_path = os.path.join(self.local_dir, key)
                    if self._should_download(obj, local_path):
                        self._download_file(key, local_path)
            
            logger.info("Sync completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Sync failed: {str(e)}")
            return False

    def _should_download(self, s3_object, local_path):
        """Determine if file needs to be downloaded"""
        if not os.path.exists(local_path):
            return True
            
        local_mtime = datetime.fromtimestamp(os.path.getmtime(local_path))
        s3_mtime = s3_object['LastModified'].replace(tzinfo=None)
        
        return (s3_object['Size'] != os.path.getsize(local_path)) or \
               (s3_mtime > local_mtime)

    def _download_file(self, s3_key, local_path):
        """Download a single file"""
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        logger.info(f"Downloading {s3_key}...")
        self.s3.download_file(self.bucket_name, s3_key, local_path)
        logger.info(f"Downloaded {s3_key}")

    def start_polling(self):
        """Start continuous sync"""
        logger.info(f"Starting sync service (polling every {self.poll_interval}s)")
        try:
            while True:
                self.sync_files()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            logger.info("Sync service stopped by user")

if __name__ == "__main__":
    try:
        sync = S3Sync(
            bucket_name='Your-Project-name',  # This will be the name of the bucket 
            local_dir='./s3_sync',
            poll_interval=60
        )
        sync.start_polling()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        exit(1)
