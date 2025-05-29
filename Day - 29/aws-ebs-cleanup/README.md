# AWS EBS Volume Cleanup

Automatically cleans up old, untagged EBS volumes in AWS.

## Features
- Identifies unused volumes older than X days
- Only targets untagged volumes
- Dry-run mode for safety
- Handles pagination for large volumes

## Usage
```bash
python ebs_cleanup.py --region us-east-1 --days 30 --dry-run
