# Import necessary libraries
from kubernetes import client, config
import time

# Function to check the readiness of another pod in the cluster
def check_pod_readiness():
    # Initialize Kubernetes client
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    # Specify the namespace and pod name of the target pod
    namespace = ""
    pod_name = "myapp"

    # Get the status of the target pod
    pod_status = v1.read_namespaced_pod_status(name=pod_name, namespace=namespace)
    
    # Check the readiness of the pod and return True or False
    return pod_status.status.conditions[0].type == "Ready"

# Function to log the health check results to a file
def log_health_check_results():
    while True:
        with open("health_check.log", "a") as file:
            result = "Pod is ready" if check_pod_readiness() else "Pod is not ready"
            file.write(f"{time.ctime()}: {result}\n")
        time.sleep(300)  # Log every 5 minutes

# Main function to run the health check application
if __name__ == "__main__":
    log_health_check_results()