# Day 23
# Challenge: Write a script to monitor Kubernetes pods and restart crashed ones.
# Focus: K8s Python client
# Example Hints: Install kubernetes lib
#!/usr/bin/env python3

import logging
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PodRestarter:
    def __init__(self, namespace):
        try:
            # Try to load in-cluster config first, fall back to kubeconfig
            config.load_incluster_config()
        except config.ConfigException:
            try:
                config.load_kube_config()
            except config.ConfigException as e:
                logger.error("Could not configure kubernetes python client")
                raise e

        self.namespace = namespace
        self.v1 = client.CoreV1Api()
        
    def get_failed_pods(self):
        """Get pods in CrashLoopBackOff or Error state"""
        failed_pods = []
        
        try:
            pods = self.v1.list_namespaced_pod(namespace=self.namespace)
            
            for pod in pods.items:
                if pod.status.phase == "Failed":
                    failed_pods.append(pod)
                    continue
                
                # Check container statuses
                if pod.status.container_statuses is None:
                    continue
                    
                for container_status in pod.status.container_statuses:
                    waiting_state = container_status.state.waiting
                    if waiting_state is not None and (
                        waiting_state.reason == "CrashLoopBackOff" or 
                        waiting_state.reason == "Error"
                    ):
                        failed_pods.append(pod)
                        break
        
        except ApiException as e:
            logger.error(f"Failed to list pods: {e}")
        
        return failed_pods
    
    def restart_pod(self, pod):
        """Delete the pod to trigger restart"""
        pod_name = pod.metadata.name
        try:
            self.v1.delete_namespaced_pod(
                name=pod_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions()
            )
            logger.info(f"Restarted pod {pod_name} in namespace {self.namespace}")
            return True
        except ApiException as e:
            logger.error(f"Failed to restart pod {pod_name}: {e}")
            return False
    
    def monitor_and_restart(self, interval_seconds=60):
        """Monitor pods and restart failed ones at regular intervals"""
        logger.info(f"Starting pod monitor for namespace {self.namespace}")
        
        while True:
            try:
                failed_pods = self.get_failed_pods()
                
                if not failed_pods:
                    logger.debug("No failed pods found")
                else:
                    logger.info(f"Found {len(failed_pods)} failed pods")
                    
                    for pod in failed_pods:
                        self.restart_pod(pod)
                
                time.sleep(interval_seconds)
            
            except Exception as e:
                logger.error(f"Unexpected error in monitoring loop: {e}")
                time.sleep(interval_seconds)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Kubernetes Pod Auto-Restarter")
    parser.add_argument(
        "--namespace",
        required=True,
        help="Kubernetes namespace to monitor"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Monitoring interval in seconds (default: 60)"
    )
    
    args = parser.parse_args()
    
    restarter = PodRestarter(args.namespace)
    restarter.monitor_and_restart(args.interval)
