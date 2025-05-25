# S3 Bucket Sync Tool

A Python script that continuously monitors an Amazon S3 bucket and syncs files to a local directory.

## Features

- Automatic periodic polling of S3 bucket (default: 60 seconds)
- Downloads only new or modified files
- Preserves S3 folder structure locally
- Detailed logging of all operations
- Configurable through code parameters

## Prerequisites

- Python 3.6+
- AWS account with S3 access
- AWS CLI configured or IAM credentials set up

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install boto3
   ```

## Configuration

Edit the following parameters in `s3_sync.py`:

```python
sync = S3Sync(
    bucket_name='your-bucket-name',  # Replace with your bucket
    local_dir='./s3_sync',           # Local sync directory
    poll_interval=60                 # Polling interval in seconds
)
```

## Usage

Run the script:
```bash
python s3_sync.py
```

The script will:
1. Connect to your S3 bucket
2. Download any existing files
3. Continuously monitor for changes

Press `Ctrl+C` to stop the service gracefully.

## Code Structure

### Key Components

1. **S3Sync Class** - Main class handling all synchronization logic
   - `__init__`: Initializes connection and verifies bucket access
   - `sync_files`: Performs one synchronization pass
   - `_should_download`: Determines if a file needs updating
   - `_download_file`: Handles actual file download
   - `start_polling`: Main loop for continuous operation

2. **Logging** - Built-in logging with timestamps

3. **Error Handling** - Comprehensive error catching and reporting

## Troubleshooting Guide

### Common Issues and Solutions

1. **Bucket Not Found (404)**
   - Symptom: `Bucket 'X' not found` error
   - Solution:
     - Verify exact bucket name
     - Check bucket exists in specified region
     - Ensure proper AWS credentials

2. **Access Denied (403)**
   - Symptom: `Access denied to bucket 'X'` error
   - Solution:
     - Verify IAM permissions (s3:ListBucket, s3:GetObject)
     - Check bucket policy

3. **Invalid Bucket Name**
   - Symptom: `InvalidBucketName` error
   - Solution:
     - Bucket names must be lowercase
     - No special characters except hyphens
     - Must be globally unique

4. **Unexpected Keyword Argument**
   - Symptom: `got an unexpected keyword argument`
   - Solution:
     - Match parameter names exactly
     - Check dictionary keys in config

5. **Missing Method Errors**
   - Symptom: `object has no attribute 'X'`
   - Solution:
     - Ensure all referenced methods exist
     - Check for typos in method names

## Security Considerations

1. **Protecting Credentials**
   - Never commit AWS credentials to code
   - Use AWS credentials file or environment variables
   - Recommended IAM policy (minimum permissions):
     ```json
     {
         "Version": "2012-10-17",
         "Statement": [
             {
                 "Effect": "Allow",
                 "Action": [
                     "s3:ListBucket",
                     "s3:GetObject"
                 ],
                 "Resource": [
                     "arn:aws:s3:::your-bucket-name",
                     "arn:aws:s3:::your-bucket-name/*"
                 ]
             }
         ]
     }
     ```

2. **Sensitive Data Handling**
   - Add `.aws/` to your `.gitignore`
   - Use environment variables for production:
     ```python
     bucket_name = os.getenv('S3_BUCKET_NAME')
     ```

## Development Notes

### Challenges Encountered

1. **Bucket Name Validation**
   - Initial attempts failed with uppercase letters
   - Solution: Enforced lowercase naming convention

2. **Region Mismatches**
   - Bucket not found despite correct name
   - Solution: Explicit region specification

3. **Permission Issues**
   - Credentials worked in CLI but not script
   - Solution: Verified IAM policy attachments

## License

MIT License - Free for personal and commercial use
