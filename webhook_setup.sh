#!/usr/bin/env bash

echo "Warning! Confirm that you run this in the same directory!"
echo "Before you run this script, make sure that you have run the setup.sh and the setup on discord!"
echo "Webhook ID: "
read webhook_id

echo "WEBHOOK_ID=$webhook_id" >> .env
