import argparse
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import time
import logging


def check_pod_status(namespace, pod_name):
    config.load_incluster_config()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    v1 = client.CoreV1Api()
    try:
        namespace = get_default_ns(namespace)
        while True:
            with open("/var/log/healthcheck_arv.log", "a") as file:
                sleeptime = 30
                pod_status = v1.read_namespaced_pod_status(
                    name=pod_name, namespace=namespace
                )
                pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
                pod_age = pod.metadata.creation_timestamp
                # Parse creation timestamp to seconds since epoch
                creation_time = time.mktime(
                    time.strptime(str(pod_age), "%Y-%m-%d %H:%M:%S%z")
                )

                # Calculate age of the container in seconds
                current_time = time.time()
                container_age_seconds = int(current_time - creation_time)

                # Format the time difference in hours, minutes, and seconds
                formatted_age = time.strftime(
                    "%d day(s) %H hour(s) %M minute(s) %S second(s)",
                    time.gmtime(container_age_seconds),
                )

                total_containers = len(pod.spec.containers)
                containers_ready = sum(
                    1 for status in pod.status.container_statuses if status.ready
                )
                start = f"***************** Pod Statuses at {time.ctime()} for {pod_name} in namespace {namespace} *******************"
                logger.info(f"\n{start}")
                file.write(f"{start}\n")
                phase = f"Status : {pod_status.status.phase}"
                phaseFie = f"Status : {pod_status.status.phase}"
                logger.info(phase)
                file.write(f"{phaseFie}\n")
                podAge = f"Pod Age : {formatted_age}"
                podAgeFile = f"Pod Age : {formatted_age}"
                logger.info(podAge)
                file.write(f"{podAgeFile}\n")
                containerReady = (
                    f"Containers Readiness : {containers_ready}/{total_containers}"
                )
                containerReadyFile = (
                    f"Containers Readiness : {containers_ready}/{total_containers}"
                )
                logger.info(containerReady)
                file.write(f"{containerReadyFile}\n")
                container_statuses = pod_status.status.container_statuses
                count = 0
                for container in container_statuses:
                    count += 1
                    startStr = f"---------------------- Container {count} Details [Start] -----------------------------"
                    logger.info(f"\n{startStr}")
                    file.write(f"{startStr}\n")
                    name = f"Container name : {container.name}"
                    nameFile = f"Container name : {container.name}"
                    logger.info(name)
                    file.write(f"{nameFile}\n")
                    id = f"Container container_id : {container.container_id}"
                    idFile = f"Container container_id : {container.container_id}"
                    logger.info(id)
                    file.write(f"{idFile}\n")
                    image = f"Container image : {container.image}"
                    imageFile = f"Container image : {container.image}"
                    logger.info(image)
                    file.write(f"{imageFile}\n")
                    restart_count = (
                        f"Container restart_count : {container.restart_count}"
                    )
                    restart_countFile = (
                        f"Container restart_count : {container.restart_count}"
                    )
                    logger.info(restart_count)
                    file.write(f"{restart_countFile}\n")
                    endStr = f"---------------------- Container {count} Details [End] -----------------------------\n"
                    logger.info(endStr)
                    file.write(endStr)
                end = f"\n***************** Sleeping for {sleeptime} seconds *******************\n"
                endFile = f"***************** Sleeping for {sleeptime} seconds *******************"
                logger.info(end)
                file.write(f"{endFile}\n")
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
