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
## Troubleshooting

### Common Issues and Solutions

#### 1. AWS Credentials Errors
**Problem**:
ConfigError: No AWS credentials found. Please configure your credentials
Solutions:

- Verify credentials are configured:

```bash
cat ~/.aws/credentials
```
- Ensure credentials are valid:

```bash
aws sts get-caller-identity
```
- If using profiles, specify the correct profile:
```bash
cloud-manager --profile your-profile ec2 list-instances
```
#### 2. Session Initialization Error
**Problem**:
ConfigError: Failed to load AWS config: Session.__init__() got an unexpected keyword argument 'config'
Solution:

- Update to the latest version of boto3:
```bash
pip install --upgrade boto3
```

#### 3. Permission Denied Errors
**Problem**:
```bash
AWSOperationError: AWS operation 'DescribeInstances' failed: You don't have permission to perform this operation
Solutions:

Verify IAM permissions for your user/role

Add required permissions to your IAM policy:

json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "s3:List*",
        "cloudwatch:Get*"
      ],
      "Resource": "*"
    }
  ]
}
```

#### 4. Client Configuration Errors
**Problem**:
TypeError: Got unexpected keyword argument 'max_attempts'
Solution:

- Ensure retry configuration is properly nested:

```python
# Correct format
Config(retries={'max_attempts': 5})
```
#### 5. Timeout Issues
**Problem**:
ReadTimeoutError: Read timeout on endpoint URL
Solutions:
```bash
Increase timeout settings:
export CLOUD_MANAGER_TIMEOUT=120
```
Or modify in code:
```bash
Config(read_timeout=120, connect_timeout=60)
```
#### 6. Python Version Compatibility
**Problem**:
SyntaxError: invalid syntax (with Python 3.6 or lower)
Solution:

- Ensure Python 3.7+ is installed:
```bash
python --version
```

- Create fresh virtual environment:

```bash
python -m venv .venv
```

- Debugging Tips
1. Enable verbose output:
```bash
cloud-manager --verbose ec2 list-instances
```

2. Check debug logs:
```bash
tail -f cloud_manager.log
```

3. Test AWS connectivity:
```bash
aws ec2 describe-instances --region us-east-1
```

4. Verify package versions:
```bash
pip list | grep -E 'boto3|click'
```

## **Contributing**
We welcome contributions! Here's how you can help:

1. **Report bugs** by opening an issue.
2. **Suggest features** via GitHub issues.
3. **Submit pull requests** for improvements.

**Guidelines:**
- Follow PEP 8 style guidelines.
- Write unit tests for new features.
- Document your changes in the README or relevant docs.

---

## **Security**
### **Reporting Security Issues**
If you discover a security vulnerability, please report it responsibly:
- Email: `kunalwaghmare1207@gmail.com`
- Do not open public GitHub issues for security-related concerns.

### **Best Practices**
- Always use IAM roles with least privilege.
- Enable MFA for AWS root accounts.
- Rotate credentials regularly.

---

## **Examples**
### **EC2 Management**
```bash
# List all running instances in JSON format
cloud-manager --output json ec2 list-instances --status running

# Stop an instance with confirmation prompt
cloud-manager ec2 stop-instance i-1234567890abcdef0 --confirm
```

### **S3 Management**
```bash
# Upload a file with public read access
cloud-manager s3 upload-file my-bucket ./file.txt --acl public-read

# List all buckets with their creation dates
cloud-manager s3 list-buckets --verbose
```

### **Monitoring**
```bash
# Monitor CPU utilization for an instance
cloud-manager monitor instance-metrics i-1234567890abcdef0 --metric CPUUtilization --period 3600

# Create a high CPU alarm
cloud-manager monitor create-alarm "HighCPU" --instance i-1234567890abcdef0 --threshold 90
```

---

## **FAQ**
### **Q: How do I specify a different AWS region?**
```bash
cloud-manager --region eu-west-1 ec2 list-instances
```

### **Q: Can I use this with AWS SSO?**
Yes! Configure your AWS profile with SSO, then use:
```bash
cloud-manager --profile sso-profile ec2 list-instances
```

### **Q: How can I export results to a file?**
```bash
cloud-manager ec2 list-instances --output json > instances.json
```

---

## **Versioning**
This project uses [Semantic Versioning](https://semver.org/). Check releases for changelog:
```bash
cloud-manager --version
```

---

## **Acknowledgments**
- Thanks to the `boto3` team for AWS SDK support.
- Inspired by [awscli](https://github.com/aws/aws-cli).

---

## **Support**
For help, please:
- Open a GitHub issue
- Email: `kunalwaghmare1207@gmail.com`

---

