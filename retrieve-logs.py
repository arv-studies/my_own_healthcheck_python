import argparse
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import time
import logging
from termcolor import colored
import paramiko


def check_pod_status(namespace, pod_name):
    config.load_incluster_config()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    v1 = client.CoreV1Api()
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    with open("/var/log/config.txt", "r") as file:
        lines = file.readlines()
        k8s_cluster_ip = lines[0].strip()
        ssh_key_path = lines[1].strip()
        username = lines[2].strip()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(k8s_cluster_ip, username=username, key_filename=ssh_key_path)

    try:
        namespace = get_default_ns(namespace)
        command = f"kubectl exec -it {pod_name} -c 'flowautomation' -n {namespace} -- tail -n 10 '/ericsson/3pp/jboss/standalone/log/server.log' >> /tmp/flowautomation.log 2>&1"
        # ssh.exec_command(command)

        stdin, stdout, stderr = ssh.exec_command(command)

        if stderr.channel.recv_exit_status() != 0:
            print("Error occurred:", stderr.read())
            logger.info("Error occurred:", stderr.read())
        else:
            print("Files retrieved successfully.")
            logger.info("Files retrieved successfully.")
        output = stdout.read().decode()
        print(output)
        logger.info(output)
        ssh.close()
        while True:
            with open("/var/log/health_check-arv.log", "a") as file:
                sleeptime = 30
                pod_status = v1.read_namespaced_pod_status(
                    name=pod_name, namespace=namespace
                )
                pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
                pod_age = pod.metadata.creation_timestamp
                total_containers = len(pod.spec.containers)
                containers_ready = sum(
                    1 for status in pod.status.container_statuses if status.ready
                )
                colrTime = colored(
                    f"{bold_start}{time.ctime()}{bold_end}", "yellow", attrs=["bold"]
                )
                colrPod_name = colored(
                    f"{bold_start}{pod_name}{bold_end}", "green", attrs=["bold"]
                )
                colrNamespace = colored(
                    f"{bold_start}{namespace}{bold_end}", "green", attrs=["bold"]
                )
                start = f"***************** Pod Statuses at {colrTime} for {colrPod_name} in namespace {colrNamespace} *******************"
                logger.info(start)
                file.write(f"{start}\n")
                phase = f"Status : {bold_start}{pod_status.status.phase}{bold_end}"
                logger.info(phase)
                file.write(f"{phase}\n")
                podAge = f"Pod Age : {bold_start}{pod_age}{bold_end}"
                logger.info(podAge)
                file.write(f"{podAge}\n")
                containerReady = f"Containers Readiness : {bold_start}{containers_ready}/{total_containers}{bold_end}"
                logger.info(containerReady)
                file.write(f"{containerReady}\n")
                # type = f"Status type  is {bold_start}{pod_status.status.conditions[0].type}{bold_end}"
                # logger.info(type)
                # file.write(f"{type}\n")
                container_statuses = pod_status.status.container_statuses
                count = 0
                for container in container_statuses:
                    count += 1
                    startStr = f"<---------------------- Container {count} Details [Start] ----------------------------->"
                    logger.info(startStr)
                    file.write(f"{startStr}\n")
                    name = f"Container name : {bold_start}{container.name}{bold_end}"
                    logger.info(name)
                    file.write(f"{name}\n")
                    id = f"Container container_id : {bold_start}{container.container_id}{bold_end}"
                    logger.info(id)
                    file.write(f"{id}\n")
                    image = f"Container image : {bold_start}{container.image}{bold_end}"
                    logger.info(image)
                    file.write(f"{image}\n")
                    restart_count = f"Container restart_count : {bold_start}{container.restart_count}{bold_end}"
                    logger.info(restart_count)
                    file.write(f"{restart_count}\n")
                    endStr = f"<---------------------- Container {count} Details [End] ----------------------------->\n"
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
        with open(
            "/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r"
        ) as file:
            arg = file.read().strip()
    return arg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check status of a pod in a specific namespace"
    )
    parser.add_argument("--namespace", help="Namespace of the pod", required=False)
    parser.add_argument("--pod-name", help="Name of the pod", required=True)

    args = parser.parse_args()

    check_pod_status(args.namespace, args.pod_name)
