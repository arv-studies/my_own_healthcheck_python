import argparse
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import time
import logging
from termcolor import colored


def check_pod_status(namespace, pod_name):
    config.load_incluster_config()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    v1 = client.CoreV1Api()
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    try:
        namespace = get_default_ns(namespace)
        while True:
            with open("/var/log/paj_logs/health_check.log", "a") as file:
                sleeptime = 30
                pod_status = v1.read_namespaced_pod_status(
                    name=pod_name, namespace=namespace)
                colrTime = colored(f"{bold_start}{time.ctime()}{bold_end}",
                                   "yellow", attrs=["bold"])
                colrPod_name = colored(f"{bold_start}{pod_name}{bold_end}",
                                       "green", attrs=["bold"])
                colrNamespace = colored(f"{bold_start}{namespace}{bold_end}",
                                        "green", attrs=["bold"])
                start = f"***************** Statuses at {colrTime} for {colrPod_name} in namespace {colrNamespace} *******************"
                logger.info(start)
                file.write(f"{start}\n")
                phase = f"Status phase  is {bold_start}{pod_status.status.phase}{bold_end}"
                logger.info(phase)
                file.write(f"{phase}\n")
                type = f"Status type  is {bold_start}{pod_status.status.conditions[0].type}{bold_end}"
                logger.info(type)
                file.write(f"{type}\n")
                container_statuses = pod_status.status.container_statuses
                for container in container_statuses:
                    startStr = f"<---------------------- Container Statuses [Start] ----------------------------->"
                    logger.info(startStr)
                    file.write(f"{startStr}\n")
                    id = f"Container container_id : {bold_start}{container.container_id}{bold_end}"
                    logger.info(id)
                    file.write(f"{id}\n")
                    image = f"Container image : {bold_start}{container.image}{bold_end}"
                    logger.info(image)
                    file.write(f"{image}\n")
                    name = f"Container name : {bold_start}{container.name}{bold_end}"
                    logger.info(name)
                    file.write(f"{name}\n")
                    restart_count = f"Container restart_count : {bold_start}{container.restart_count}{bold_end}"
                    logger.info(restart_count)
                    file.write(f"{restart_count}\n")
                    endStr = f"<---------------------- Container Statuses [End] ----------------------------->\n"
                    logger.info(endStr)
                    file.write(f"{endStr}\n")
                end = f"***************** Sleeping for {bold_start}{sleeptime}{bold_end} seconds *******************\n"
                logger.info(end)
                file.write(f"{end}\n")
            time.sleep(sleeptime)
    except Exception as e:
        logger.info(f"Error: {e}")


def get_default_ns(arg):
    if not arg:
        with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as file:
            arg = file.read().strip()
    return arg


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Check status of a pod in a specific namespace')
    parser.add_argument(
        '--namespace', help='Namespace of the pod', required=False)
    parser.add_argument('--pod-name', help='Name of the pod', required=True)

    args = parser.parse_args()

    check_pod_status(args.namespace, args.pod_name)
