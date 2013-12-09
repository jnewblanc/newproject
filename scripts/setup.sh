#!/bin/sh
#
# Dummy script to simulate the setup script
#

envfile=".env"

echo "Setting up the test project"
if [ ! -f "${envfile}" ]; then
  echo "project=test" > ${envfile}
fi
echo "Done"


