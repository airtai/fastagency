#!/bin/bash

# Set the threshold for certificate expiration (in days)
THRESHOLD=15

# Check if certificate is expiring within the threshold
expiry_str=$(ssh -o StrictHostKeyChecking=no -i key.pem azureuser@"$DOMAIN" "sudo openssl x509 -in /etc/letsencrypt/live/$DOMAIN/fullchain.pem -noout -enddate | cut -d= -f2")
expiration_date=$(date -d "$expiry_str" +%s)
current_date=$(date +%s)
days_until_expiry=$(( (expiration_date - current_date) / 86400 ))

if [ "$days_until_expiry" -le "$THRESHOLD" ]; then
    echo "Certificate for $DOMAIN is expiring in $days_until_expiry days. PLEASE RENEW ASAP."
    exit -1
else
    echo "Certificate for $DOMAIN is not expiring within the next $THRESHOLD days. Expires after $days_until_expiry days. No action needed."
fi
