# cloud_manager/utils/exceptions.py
class CloudManagerError(Exception):
    """Base exception for all cloud manager errors"""
    pass

class ConfigError(CloudManagerError):
    """Configuration related errors"""
    pass

class AWSOperationError(CloudManagerError):
    """AWS operation failures"""
    def __init__(self, operation: str, message: str, aws_code: str = None):
        self.operation = operation
        self.aws_code = aws_code
        super().__init__(f"AWS operation '{operation}' failed: {message}")

def handle_aws_error(error: Exception, operation_name: str) -> None:
    """Handle AWS errors and convert to appropriate exceptions"""
    error_code = getattr(error, 'response', {}).get('Error', {}).get('Code', 'Unknown')
    error_msg = str(error)
    
    if error_code == 'UnauthorizedOperation':
        raise AWSOperationError(
            operation_name,
            "You don't have permission to perform this operation",
            error_code
        )
    elif error_code == 'ResourceNotFoundException':
        raise AWSOperationError(
            operation_name,
            "The requested resource was not found",
            error_code
        )
    else:
        raise AWSOperationError(
            operation_name,
            f"AWS error occurred: {error_msg}",
            error_code
        )
