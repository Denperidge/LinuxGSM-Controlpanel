#!/bin/bash

script=$(readlink -f $0)
lgsmcp="$(dirname "${script}")/lgsmcp"

echo "Installing requirements..."
sudo apt install python3-pip
pip3 install -r requirements.txt


echo "Generating .env file..."
${lgsmcp}/../env.sh

echo "Collecting static files..."
python3 "${lgsmcp}/manage.py" collectstatic --noinput

echo "Generating database..."
python3 "${lgsmcp}/manage.py" migrate --run-syncdb

echo "Creating new superuser..."

read -p "Identifier: " identifier
read -s -p "Password: " password

python3 "${lgsmcp}/manage.py" createsuperuser --identifier=${identifier} --linux_username= --lgsm_servername= --password=${password}