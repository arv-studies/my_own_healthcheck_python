import argparse
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import time
import logging
from termcolor import colored


def check_deployment_status(namespace, deployment_name):
    config.load_incluster_config()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    v1 = client.CoreV1Api()
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    try:
        namespace = get_default_ns(namespace)
        while True:
            with open("/var/log/healthcheck_deployment_arv.log", "a") as file:
                sleeptime = 30
                deployment = v1.read_namespaced_deployment(
                    name=deployment_name, namespace=namespace, pretty="true"
                )
                deployment_status = deployment.status
                logger.info(f"\nDeployment '{deployment_name}' Status:")
                file.write(f"Deployment '{deployment_name}' Status:\n")

                logger.info(f"  Replicas: {deployment_status.replicas}")
                file.write(f"  Replicas: {deployment_status.replicas}")
                logger.info(f"  Updated Replicas: {deployment_status.updated_replicas}")
                file.write(f"  Updated Replicas: {deployment_status.updated_replicas}")
                logger.info(
                    f"  Available Replicas: {deployment_status.available_replicas}"
                )
                file.write(
                    f"  Available Replicas: {deployment_status.available_replicas}"
                )
                logger.info(
                    f"  Unavailable Replicas: {deployment_status.unavailable_replicas}"
                )
                file.write(
                    f"  Unavailable Replicas: {deployment_status.unavailable_replicas}"
                )
                logger.info("\nContainer Statuses:")
                for container_status in deployment_status.container_statuses:
                    file.write(f"  Container Name: {container_status.name}")
                    logger.info(f"    Ready: {container_status.ready}")
                    file.write(f"    Restart Count: {container_status.restart_count}")

                    logger.info(f"  Container Name: {container_status.name}")
                    file.write(f"    Ready: {container_status.ready}")
                    logger.info(f"    Restart Count: {container_status.restart_count}")
                if container_status.state:
                    file.write(f"    State: {container_status.state}")
                    logger.info(f"    State: {container_status.state}")
            time.sleep(sleeptime)
    except Exception as e:
        logger.info(f"Error: {e}")


def get_default_ns(arg):
    if not arg:
        with open(
            "/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r"
        ) as file:
            arg = file.read().strip()
    return arg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check status of a deployment in a specific namespace"
    )
    parser.add_argument(
        "--namespace", help="Namespace of the deployment", required=False
    )
    parser.add_argument(
        "--deployment_name", help="Name of the deployment", required=True
    )

    args = parser.parse_args()

    check_deployment_status(args.namespace, args.deployment_name)
