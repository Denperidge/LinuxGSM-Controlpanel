#!/bin/bash

script=$(readlink -f $0)
lgsmcp="$(dirname "${script}")/lgsmcp"

read -p "This will wipe the entire db, including migrations and caching. If you're certain, type 'yes': " certain

if [ "${certain}" != "yes" ]; then
    echo "Wipe cancelled!"
    exit 0
fi

rm -rf "${lgsmcp}/controlpanel/__pycache__/"
rm -rf "${lgsmcp}/controlpanel/migrations/"
rm -rf "${lgsmcp}/lgsmcp/__pycache__/"
rm -rf "${lgsmcp}/lgsmcp/migrations/"
rm "${lgsmcp}/db.sqlite3"
rm "${lgsmcp}/db.sqlite3*"

echo "Wiped cache, migrations and db!"
echo "Wipe succesful!"

echo "Reinstalling..."
${lgsmcp}/../install.sh
echo "Reinstalled!"

exit 0
