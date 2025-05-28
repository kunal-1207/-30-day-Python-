import docker
from datetime import datetime
import logging
import sys

# Configure logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('container_uptime.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('docker_uptime')

def get_container_uptime(container):
    """Calculate and return container uptime in human-readable format"""
    try:
        stats = container.stats(stream=False)
        started_at = stats['read'][:26]  # Get the first 26 chars to parse datetime
        start_time = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%S.%f')
        uptime = datetime.utcnow() - start_time
        
        # Convert uptime to human readable format
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{days}d {hours}h {minutes}m {seconds}s"
    except Exception as e:
        logger.error(f"Error calculating uptime: {str(e)}")
        return "N/A"

def log_running_containers():
    try:
        logger.info("Attempting to connect to Docker...")
        client = docker.from_env()
        logger.info("Successfully connected to Docker")
        
        running_containers = client.containers.list()
        
        if not running_containers:
            logger.info("No running containers found.")
            return
            
        logger.info(f"Found {len(running_containers)} running containers:")
        
        for container in running_containers:
            try:
                uptime = get_container_uptime(container)
                logger.info(
                    f"Container ID: {container.short_id}, "
                    f"Name: {container.name}, "
                    f"Image: {container.image.tags[0] if container.image.tags else 'None'}, "
                    f"Status: {container.status}, "
                    f"Uptime: {uptime}"
                )
            except Exception as e:
                logger.error(f"Error processing container {container.short_id}: {str(e)}")
                
    except docker.errors.DockerException as e:
        logger.error(f"Docker connection error: {str(e)}")
        logger.error("Please ensure Docker is running and your user has permissions.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    log_running_containers()
