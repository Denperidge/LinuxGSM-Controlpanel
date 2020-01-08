#!/bin/bash

script=$(readlink -f $0)
lgsmcp="$(dirname "${script}")/lgsmcp"

echo "Installing requirements..."
py -3 -m pip install -r requirements.txt

echo "Generating database..."

py -3 "${lgsmcp}/manage.py" migrate --run-syncdb

echo "Creating new superuser..."

read -p "Identifier: " identifier
read -s -p "Password: " password

py -3 "${lgsmcp}/manage.py" createsuperuser --identifier=${identifier} --linux_username= --lgsm_servername= --password=${password}