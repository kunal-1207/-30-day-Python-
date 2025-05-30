# cloud_manager/config.py
import os
from typing import Optional, Dict, Any
from botocore.exceptions import ProfileNotFound, NoCredentialsError
from .utils.logging import get_logger
from .utils.exceptions import ConfigError
from .utils.aws import AWSSessionManager

logger = get_logger(__name__)

class CloudManagerConfig:
    def __init__(self, profile_name: str = 'default', region: str = 'ap-south-1', verbose: bool = False):
        self.profile_name = profile_name
        self.region = region
        self.verbose = verbose
        self._aws_manager: Optional[AWSSessionManager] = None
        self._additional_config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load and validate AWS configuration using the session manager"""
        try:
            self._aws_manager = AWSSessionManager(
                profile_name=self.profile_name,
                region_name=self.region
            )
            
            # Initialize commonly used clients with proper configuration
            self.ec2_client = self._aws_manager.get_client('ec2')
            self.s3_client = self._aws_manager.get_client('s3')
            self.cloudwatch_client = self._aws_manager.get_client('cloudwatch')
            
            self._load_env_config()
            
            logger.info(
                f"Successfully loaded config for profile '{self.profile_name}' "
                f"in region '{self.region}' with AWS account ID: {self.account_id}"
            )
            
        except ProfileNotFound as e:
            raise ConfigError(f"AWS profile '{self.profile_name}' not found")
        except NoCredentialsError as e:
            raise ConfigError("No AWS credentials found. Please configure your credentials")
        except Exception as e:
            raise ConfigError(f"Failed to load AWS config: {str(e)}")

    def _load_env_config(self) -> None:
        """Load additional configuration from environment variables"""
        self._additional_config = {
            'debug_mode': os.getenv('CLOUD_MANAGER_DEBUG', 'false').lower() == 'true',
            'default_output': os.getenv('CLOUD_MANAGER_OUTPUT', 'text')
        }

    @property
    def current_region(self) -> str:
        return self.region

    @property
    def current_profile(self) -> str:
        return self.profile_name

    @property
    def account_id(self) -> str:
        if not self._aws_manager:
            raise ConfigError("AWS session not initialized")
        return self._aws_manager.get_aws_account_id()

    @property
    def aws_manager(self) -> AWSSessionManager:
        if not self._aws_manager:
            raise ConfigError("AWS session not initialized")
        return self._aws_manager

    def get_config_value(self, key: str, default: Any = None) -> Any:
        return self._additional_config.get(key, default)

def load_config(profile_name: str, region: str, verbose: bool) -> CloudManagerConfig:
    return CloudManagerConfig(profile_name, region, verbose)
