#!/bin/bash

script=$(readlink -f $0)
lgsmcp="$(dirname "${script}")/lgsmcp"

echo "Installing requirements..."
py -3 -m pip install -r requirements.txt

echo "Generating .env file..."
echo "To secure the connection between Django and the Daemon, a hmac key needs to be applied."
echo "Supply a random passphrase, which will then be hashed into a sha1 and placed in .env"
read -p "HMAC Passphrase: " passphrase
hmacoutput=$(echo -n "value" | openssl dgst -sha1 -hmac "${passphrase}")
hmac=$(echo ${hmacoutput/(stdin)= /})
echo -n "DAEMON_HMAC=" > .env
echo $hmac >> .env

echo "Generating database..."

py -3 "${lgsmcp}/manage.py" migrate --run-syncdb

echo "Creating new superuser..."

read -p "Identifier: " identifier
read -s -p "Password: " password

py -3 "${lgsmcp}/manage.py" createsuperuser --identifier=${identifier} --linux_username= --lgsm_servername= --password=${password}