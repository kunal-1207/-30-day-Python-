# EC2 Instance Status Fetching Program

## Overview

This Python program interacts with AWS EC2 using the Boto3 SDK to fetch the statuses of EC2 instances in a specified region. It includes two primary functionalities:

1. Listing all EC2 instances in a specified AWS region and displaying their instance IDs and states.
2. Fetching detailed status information for each EC2 instance, including instance state, instance status, and system status.

## Prerequisites

* Python 3.x installed
* AWS credentials (Access Key ID, Secret Access Key, and optionally, a session token)
* Boto3 installed (`pip install boto3`)

## How to Run the Program

1. Ensure that you have Python and Boto3 installed.
2. Configure your AWS credentials using AWS CLI or by setting environment variables.
3. Run the program using the command:

   ```bash
   python <filename.py>
   ```

## Program Breakdown

### Importing Required Libraries

```python
import logging
import boto3
```

* `logging`: Used to handle warning and error messages.
* `boto3`: AWS SDK for Python, used to interact with EC2 and other AWS services.

### Function: `get_ec2_instance_statuses`

This function fetches the statuses of all EC2 instances in the specified region.

#### Parameters:

* `region_name`: AWS region to connect to (default is 'ap-south-1').
* `aws_access_key_id`, `aws_secret_access_key`, `aws_session_token`: Optional AWS credentials.

#### Function Logic:

* A Boto3 EC2 client is created using the provided credentials and region.
* The paginator is used to handle multiple response pages from the `describe_instance_status` API.
* For each page of results, the instance status information is processed and stored in a list.
* If certain keys are missing in the response, a warning is logged.
* The function returns a list of instance status dictionaries.

### Function: `list_all_ec2_instances`

This function lists all EC2 instances in the specified region and their states.

#### Parameters:

* `region_name`: AWS region to connect to (default is 'ap-south-1').

#### Function Logic:

* A Boto3 EC2 client is created for the specified region.
* The `describe_instances` API is called to get all EC2 instances in the region.
* The function iterates through reservations and instances, printing instance IDs and states.

### Main Execution Block

```python
if __name__ == "__main__":
```

* When the script is run directly, it first lists all EC2 instances and then fetches the status of each instance.
* The results are printed to the console.

## Error Handling

* Exceptions are caught and logged using the `logging.error()` method to provide informative error messages.

## Example Output

```
Checking all EC2 instances in ap-south-1:
InstanceId: i-0abcd1234efgh5678, State: running

Checking instance statuses:
[{'InstanceId': 'i-0abcd1234efgh5678', 'InstanceState': 'running', 'InstanceStatus': 'ok', 'SystemStatus': 'ok'}]
```

## Additional Notes

* Ensure that the AWS region specified is correct.
* The user must have appropriate IAM permissions to access EC2 instance information.
