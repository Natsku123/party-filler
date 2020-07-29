#!/usr/bin/env bash

echo "Warning! Confirm that you run this in the same directory!"

# TODO add update download

docker exec partyfiller_backend_1 flask db migrate -m "Update migration."
docker exec partyfiller_backend_1 flask db upgrade