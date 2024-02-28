from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
import logging
import argparse


def check_pod_status(namespace, pod_name, container_name):
    config.load_incluster_config()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Create an instance of the CoreV1Api
    v1 = client.CoreV1Api()
    namespace = get_default_ns(namespace)
    container_name = get_default_container(container_name)
    file_path = "/ericsson/3pp/jboss/standalone/log/server.log"

    try:
        # Read the contents of the file inside the container
        list = v1.list_namespaced_pod(namespace)

        for item in list.items:
            print(item.metadata.name)

        # Executing commands
        exec_command = [
            "sh", "-c", "echo welcome && ls && cat /ericsson/3pp/jboss/standalone/log/server.log > /var/log/paj_logs/server.log"]
        resp = stream(v1.connect_get_namespaced_pod_exec, pod_name,
                      namespace, command=exec_command, container=container_name)
        print("*****************************")
        for line in resp:
            print(line, end="")
            logger.info(f"{line}")
        logger.info("*****************************")
    except ApiException as e:
        print(
            f"Exception when calling CoreV1Api->connect_get_namespaced_pod_exec: {e}")


def get_default_ns(arg):
    if not arg:  # Check if the string argument is empty
        with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as file:
            arg = file.read().strip()  # Read and strip any leading/trailing whitespaces
    return arg


def get_default_container(arg):
    if not arg:  # Check if the string argument is empty
        arg = "flowautomation"
    return arg


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Check status of a pod in a specific namespace')
    parser.add_argument(
        '--namespace', help='Namespace of the pod', required=False)
    parser.add_argument('--pod-name', help='Name of the pod', required=True)
    parser.add_argument('--container-name',
                        help='Name of the container', required=False)

    args = parser.parse_args()

    check_pod_status(args.namespace, args.pod_name, args.container_name)
