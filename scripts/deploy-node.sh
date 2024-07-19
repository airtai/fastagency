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
check_variable "GITHUB_USERNAME"
check_variable "GITHUB_PASSWORD"
check_variable "NODE_DOMAIN"
check_variable "PORT"
check_variable "DATABASE_URL"
check_variable "WASP_WEB_CLIENT_URL"
check_variable "JWT_SECRET"
check_variable "GOOGLE_CLIENT_ID"
check_variable "GOOGLE_CLIENT_SECRET"
check_variable "WASP_SERVER_URL"
check_variable "FASTAGENCY_SERVER_URL"
check_variable "WASP_NATS_PASSWORD"



if [ ! -f key.pem ]; then
    echo "ERROR: key.pem file not found"
    exit -1
fi


ssh_command="ssh -o StrictHostKeyChecking=no -i key.pem azureuser@$NODE_DOMAIN"

container_name="wasp-backend"
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
$ssh_command "docker pull ghcr.io/airtai/fastagency-studio-node:'$TAG'"
sleep 10

echo "Deleting old image"
$ssh_command "docker system prune -f || echo 'No images to delete'"

echo "INFO: starting docker container"
$ssh_command "docker run --name $container_name -p $PORT:$PORT -e PORT='$PORT' \
    -e DATABASE_URL='$DATABASE_URL' -e WASP_WEB_CLIENT_URL='$WASP_WEB_CLIENT_URL' \
	-e JWT_SECRET='$JWT_SECRET' -e GOOGLE_CLIENT_ID='$GOOGLE_CLIENT_ID' \
	-e GOOGLE_CLIENT_SECRET='$GOOGLE_CLIENT_SECRET' \
    -e WASP_SERVER_URL='$WASP_SERVER_URL' \
    -e FASTAGENCY_SERVER_URL='$FASTAGENCY_SERVER_URL' \
    -e ADMIN_EMAILS='$ADMIN_EMAILS' -e WASP_NATS_PASSWORD='$WASP_NATS_PASSWORD' \
    --restart always \
	-d ghcr.io/airtai/fastagency-studio-node:$TAG"
