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
            with open("/var/log/error.log", "a") as file:
                sleeptime = 30
                pod_status = v1.read_namespaced_pod_status(
                    name=pod_name, namespace=namespace
                )
                pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
                pod_age = pod.metadata.creation_timestamp

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
                colrTime = colored(f"{time.ctime()}", "yellow", attrs=["bold"])
                colrPod_name = colored(f"{pod_name}", "green", attrs=["bold"])
                colrNamespace = colored(f"{namespace}", "green", attrs=["bold"])
                bullet_point = chr(8226)
                start = f" {bullet_point* 8} Pod Statuses at {bold_start}'{colrTime}'{bold_end} for {bold_start}'{colrPod_name}'{bold_end} in namespace {bold_start}'{colrNamespace}'{bold_end} {bullet_point* 8} "
                startFile = f" {bullet_point* 8} Pod Statuses at '{time.ctime()}' for '{pod_name}' in namespace '{namespace}' {bullet_point* 8} "
                logger.info(f"\n{start}")
                file.write(f"{startFile}\n")

                colrPhaseKey = colored(f"Status : ", "red", attrs=["bold"])
                colrPhaseVal = colored(
                    f"{pod_status.status.phase}", "green", attrs=["bold"]
                )
                phase = f"{colrPhaseKey}{colrPhaseVal}"
                logger.info(phase)
                file.write(f"{phase}\n")

                formatted_ageKey = colored(f"Pod Age : ", "red", attrs=["bold"])
                formatted_ageVal = colored(f"{formatted_age}", "green", attrs=["bold"])
                podAge = f"{formatted_ageKey}{formatted_ageVal}"

                # podAge = f"{formatted_age}"
                # colrAge = colored(f"{podAge}", "green", attrs=["bold"])
                # podAgeFile = f"Pod Age : {formatted_age}"
                logger.info(podAge)
                file.write(f"{podAge}\n")

                containers_readyKey = colored(
                    f"Containers Readiness : ", "red", attrs=["bold"]
                )
                containers_readyVal = colored(
                    f"{containers_ready}/{total_containers}", "green", attrs=["bold"]
                )
                containerReady = f"{containers_readyKey}{containers_readyVal}"

                logger.info(containerReady)
                file.write(f"{containerReady}\n")
                container_statuses = pod_status.status.container_statuses
                count = 0
                for container in container_statuses:
                    count += 1
                    startStr = f"\n ---------------- Container {count} Properties [Start] ---------------- "
                    colrStartStr = colored(f"{startStr}", "blue")
                    logger.info(f"{colrStartStr}")
                    file.write(f"{startStr}\n")

                    nameKey = colored(f"Name : ", "green", attrs=["bold"])
                    nameVal = colored(f"{container.name}", "red", attrs=["bold"])
                    name = f"{nameKey}{nameVal}"
                    logger.info(name)
                    file.write(f"{name}\n")

                    idKey = colored(f"container_id : ", "green", attrs=["bold"])
                    idVal = colored(f"{container.container_id}", "red", attrs=["bold"])
                    id = f"{idKey}{idVal}"

                    logger.info(id)
                    file.write(f"{id}\n")

                    imageKey = colored(f"Image : ", "green", attrs=["bold"])
                    imageVal = colored(f"{container.image}", "red", attrs=["bold"])
                    image = f"{imageKey}{imageVal}"

                    logger.info(image)
                    file.write(f"{image}\n")

                    restart_countKey = colored(
                        f"restart_count : ", "green", attrs=["bold"]
                    )
                    restart_countVal = colored(
                        f"{container.restart_count}", "red", attrs=["bold"]
                    )
                    restart_count = f"{restart_countKey}{restart_countVal}"

                    logger.info(restart_count)
                    file.write(f"{restart_count}\n")

                    endStr = f" ---------------- Container {count} Properties [End] ---------------- \n"
                    colrendStr = colored(f"{endStr}", "blue")
                    logger.info(colrendStr)
                    file.write(f"{endStr}\n")
                sleep = f" ****************** Sleeping for {sleeptime} seconds ****************** \n"
                colrSleep = colored(f"{sleep}", "yellow", attrs=["blink"])
                logger.info(f"\n{colrSleep}")
                file.write(f"{sleep}\n")
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
