#!/bin/bash


# Check if variables are defined
check_variable() {
    if [ -z "${!1}" ]; then
        echo "ERROR: $1 variable must be defined, exiting"
        exit -1
    fi
}

# Check for required variables
check_variable "TAG"
check_variable "DOMAIN"
check_variable "DATABASE_URL"
check_variable "PY_DATABASE_URL"
check_variable "AUTH_NATS_PASSWORD"
check_variable "NATS_PRIV_NKEY"

if [[ "$TAG" != "latest" && "$TAG" != "dev" ]]; then
    echo "Error: TAG value is not 'dev' or 'latest'. It is '$TAG'. Exiting."
    exit -1
fi


if [ ! -f key.pem ]; then
    echo "ERROR: key.pem file not found"
    exit -1
fi


ssh_command="ssh -o StrictHostKeyChecking=no -i key.pem azureuser@$DOMAIN"

container_name="auth-callout"
log_file="${container_name}.log"

echo "INFO: Capturing docker container logs"
$ssh_command "docker logs $container_name >> $log_file 2>&1 || echo 'No container logs to capture'"

# Check if log file size exceeds 1GB (1073741824 bytes) and trim if necessary
$ssh_command "if [ \$(stat -c%s \"$log_file\") -ge 1073741824 ]; then echo 'Log file size exceeds 1GB, trimming...'; tail -c 1073741824 \"$log_file\" > \"$log_file.tmp\" && mv \"$log_file.tmp\" \"$log_file\"; fi"

echo "INFO: stopping already running docker container"
$ssh_command "docker stop $container_name || echo 'No containers available to stop'"
$ssh_command "docker container prune -f || echo 'No stopped containers to delete'"

echo "INFO: pulling docker image"
$ssh_command "echo $GITHUB_PASSWORD | docker login -u '$GITHUB_USERNAME' --password-stdin '$REGISTRY'"
$ssh_command "docker pull ghcr.io/airtai/fastagency-studio-auth-callout:'$TAG'"
sleep 10

echo "Deleting old image"
$ssh_command "docker system prune -f || echo 'No images to delete'"

echo "INFO: starting docker container"
$ssh_command "docker run --name $container_name \
    -e DATABASE_URL='$DATABASE_URL' -e PY_DATABASE_URL='$PY_DATABASE_URL' \
	-e AUTH_NATS_PASSWORD='$AUTH_NATS_PASSWORD' -e NATS_PRIV_NKEY='$NATS_PRIV_NKEY' \
	-e DOMAIN='$DOMAIN' \
    --restart always \
	-d ghcr.io/airtai/fastagency-studio-auth-callout:$TAG"
