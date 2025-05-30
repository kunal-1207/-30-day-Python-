# cloud_manager/utils/aws.py
"""
AWS utility module for managing sessions and clients
with enhanced configuration and error handling.
"""
import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from typing import Optional, Dict, Any
from .logging import get_logger
from .exceptions import AWSOperationError

logger = get_logger(__name__)

class AWSSessionManager:
    """
    Centralized AWS session and client manager with:
    - Automatic retry configuration
    - Custom timeouts
    - Secure credential handling
    - Client caching
    """
    
    def __init__(self, profile_name: str = None, region_name: str = 'us-east-1'):
        """
        Initialize AWS session manager.
        
        Args:
            profile_name: AWS profile name (optional)
            region_name: AWS region (default: us-east-1)
        """
        self.profile_name = profile_name
        self.region_name = region_name
        self._session = None
        self._clients = {}
        
        # Default configuration with retries and timeouts
        self._boto_config = Config(
            retries={
                'max_attempts': 5,
                'mode': 'adaptive'
            },
            connect_timeout=30,
            read_timeout=60
        )
        
        self._initialize_session()
    
    def _initialize_session(self) -> None:
        """Initialize the AWS session with proper error handling."""
        try:
            session_args = {
                'region_name': self.region_name
            }
            
            if self.profile_name:
                session_args['profile_name'] = self.profile_name
            
            self._session = boto3.Session(**session_args)
            
            # Verify credentials are valid
            sts = self._session.client('sts', config=self._boto_config)
            sts.get_caller_identity()
            
            logger.info(
                f"AWS session initialized for profile '{self.profile_name or 'default'}' "
                f"in region '{self.region_name}'"
            )
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidClientTokenId':
                raise AWSOperationError(
                    'SessionInitialization',
                    'Invalid AWS credentials. Please configure your credentials.',
                    error_code
                )
            raise
        except BotoCoreError as e:
            raise AWSOperationError(
                'SessionInitialization',
                f"Failed to initialize AWS session: {str(e)}"
            )
    
    def get_client(self, service_name: str, **kwargs) -> Any:
        """
        Get a cached AWS service client or create a new one.
        
        Args:
            service_name: AWS service name (e.g., 'ec2', 's3')
            kwargs: Additional client configuration
            
        Returns:
            AWS service client
        """
        cache_key = (service_name, frozenset(kwargs.items()))
        
        if cache_key not in self._clients:
            try:
                # Create a new config with default settings
                client_config = Config(
                    retries=self._boto_config.retries,
                    connect_timeout=self._boto_config.connect_timeout,
                    read_timeout=self._boto_config.read_timeout
                )
                
                self._clients[cache_key] = self._session.client(
                    service_name,
                    config=client_config
                )
                logger.debug(f"Created new client for {service_name}")
            except Exception as e:
                raise AWSOperationError(
                    'ClientInitialization',
                    f"Failed to create {service_name} client: {str(e)}"
                )
        
        return self._clients[cache_key]
    
    def get_resource(self, service_name: str, **kwargs) -> Any:
        """
        Get an AWS service resource with proper configuration.
        
        Args:
            service_name: AWS service name (e.g., 'ec2', 's3')
            kwargs: Additional resource configuration
            
        Returns:
            AWS service resource
        """
        try:
            resource_config = Config(
                retries=self._boto_config.retries,
                connect_timeout=self._boto_config.connect_timeout,
                read_timeout=self._boto_config.read_timeout
            )
                
            return self._session.resource(
                service_name,
                config=resource_config
            )
        except Exception as e:
            raise AWSOperationError(
                'ResourceInitialization',
                f"Failed to create {service_name} resource: {str(e)}"
            )
    
    def get_aws_account_id(self) -> str:
        """Get the AWS account ID for the current session."""
        sts = self.get_client('sts')
        return sts.get_caller_identity()['Account']
    
    @property
    def current_region(self) -> str:
        """Get current AWS region."""
        return self.region_name
    
    @property
    def current_profile(self) -> Optional[str]:
        """Get current AWS profile name."""
        return self.profile_name
