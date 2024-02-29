# Python script to read SSH connection information from a file inside a mounted volume in a Kubernetes cluster

import paramiko

# Read SSH connection information from a file inside the mounted volume
with open("/var/log/config.txt", "r") as file:
    lines = file.readlines()
    k8s_cluster_ip = lines[0].strip()
    ssh_key_path = lines[1].strip()
    username = lines[2].strip()

# Connect to the Kubernetes cluster
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(k8s_cluster_ip, username=username, key_filename=ssh_key_path)

# Command to access the pod and container to retrieve files (replace POD_NAME and CONTAINER_NAME with actual names)
command = "kubectl exec -it POD_NAME -c CONTAINER_NAME -- cat /path/to/file > local_file"

# Execute the command
stdin, stdout, stderr = ssh.exec_command(command)

# Check for any errors
if stderr.channel.recv_exit_status() != 0:
    print("Error occurred:", stderr.read())
else:
    print("Files retrieved successfully.")

# Close the SSH connection
ssh.close()
