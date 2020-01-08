#!/bin/bash

script=$(readlink -f $0)
lgsmcp="$(dirname "${script}")/lgsmcp"

read -p "This will wipe the entire db, including migrations and caching. If you're certain, type 'yes': " certain


if [ "${certain}" != "yes" ]; then
    echo "Wipe cancelled!"
    sleep 2
    exit 0
fi

rm -rf "${lgsmcp}/controlpanel/__pycache__/"
rm -rf "${lgsmcp}/controlpanel/migrations/"
rm -rf "${lgsmcp}/lgsmcp/__pycache__/"
rm -rf "${lgsmcp}/lgsmcp/migrations/"
rm "${lgsmcp}/db.sqlite3"
rm "${lgsmcp}/db.sqlite3*"

echo "Wiped cache, migrations and db!"

sleep 1

echo "Creating new superuser..."

python "${lgsmcp}/manage.py" migrate --run-syncdb
python "${lgsmcp}/manage.py" createsuperuser --linux_username= --lgsm_servername=

echo "Wipe succesful!"

sleep 5
exit 0
