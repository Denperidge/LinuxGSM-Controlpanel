#!/bin/bash

echo "To secure the connection between Django and the Daemon, a hmac key needs to be applied."
echo "Supply a random passphrase, which will then be hashed into a sha1 and placed in .env"
read -p "HMAC Passphrase: " passphrase
hmacoutput=$(echo -n "value" | openssl dgst -sha1 -hmac "${passphrase}")
hmac=$(echo ${hmacoutput/(stdin)= /})
echo -n "DAEMON_HMAC=" > .env
echo $hmac >> .env

echo "Add allowed hosts (which can be used to connect to the controlpanel). Simply enter an IP address or domain name, no port."
echo "Leave empty to stop adding hosts"
echo -n "ALLOWED_HOSTS=" >> .env
host="placeholder"
seperator=""
while [ ! -z "$host" ]
do
    read -p "Allowed host: " host
    if [ ! -z "$host" ]; then echo -n "${seperator}${host}" >> .env; fi
    
    seperator=","
done

echo >> .env  # Add newline
echo "#DEBUG=true # Uncomment this line to enable debugging. Do NOT use in production." >> .env
