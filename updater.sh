#!/bin/bash

set -e

rm -f update-errors.log
git checkout main

if git pull 2> update-errors.log | grep -q 'Already up to date.'; then
   echo "Already up to date"
   exit 0
fi

if grep -q "error" update-errors.log; then
   echo "error occurred when updating, check update-errors.log"
   exit 1
fi

sudo systemctl restart radiopi.service
echo "Radiopi updated and restarted."