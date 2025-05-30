# Cloud Resource Manager CLI

A Python CLI tool to manage AWS cloud resources (EC2, S3, and Monitoring) with robust error handling and logging.

## Features

- **EC2 Management**:
  - List instances (running/stopped/all)
  - Start/stop/terminate instances
  - View instance details

- **S3 Management**:
  - List buckets
  - Upload/download files
  - Manage bucket policies

- **Monitoring**:
  - View CloudWatch metrics
  - Set up basic alarms
  - Monitor resource utilization

## Installation

1. **Prerequisites**:
   - Python 3.7+
   - AWS credentials configured (~/.aws/credentials)

2. **Install from source**:
   ```bash
   git clone https://github.com/yourusername/cloud-manager.git
   cd cloud-manager
   pip install -e .
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Set up AWS credentials:
   ```bash
   aws configure
   ```

2. Environment variables (optional):
   ```bash
   export CLOUD_MANAGER_DEBUG=true  # Enable debug logging
   export CLOUD_MANAGER_OUTPUT=json  # Set default output format
   ```

## Usage

```bash
# General syntax
cloud-manager [--profile PROFILE] [--region REGION] [--verbose] <command> [options]

# Examples:
# List EC2 instances
cloud-manager ec2 list-instances

# Upload file to S3
cloud-manager s3 upload-file my-bucket ./local-file.txt

# Get instance metrics
cloud-manager monitor instance-metrics i-1234567890abcdef0

# Show account info
cloud-manager ec2 show-account
```

## Command Reference

### EC2 Commands
```
list-instances    List EC2 instances
show-account      Display AWS account information
start-instance    Start an EC2 instance
stop-instance     Stop an EC2 instance
```

### S3 Commands
```
list-buckets      List S3 buckets
upload-file       Upload file to S3 bucket
download-file     Download file from S3 bucket
```

### Monitoring Commands
```
instance-metrics  Get CloudWatch metrics for EC2 instance
create-alarm      Create CloudWatch alarm
```

## Development

1. **Setup development environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   pip install -e .[dev]
   ```

2. **Run tests**:
   ```bash
   pytest
   ```

3. **Code formatting**:
   ```bash
   black .
   flake8
   ```
