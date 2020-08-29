#!/usr/bin/env bash

echo "Warning! Confirm that you run this in the same directory!"
echo "Database name: "
read database
echo "Database user: "
read db_user
echo "Database password: "
read db_pass
echo "Database root password: "
read root_pass
echo "Discord Client ID: "
read client_id
echo "Discord Client Secret: "
read client_secret
echo "Hostname for API: "
read api_hostname
echo "Hostname for site: "
read site_hostname
echo "Secret for Flask: "
read flask_secret
echo "Discord Bot token: "
read bot_token
echo "Bot owner (Discord ID): "
read bot_owner
echo "Debug / default channel (Discord ID): "
read debug_channel
echo "DATABASE=$database" >> .env
echo "DB_USER=$db_user" >> .env
echo "DB_PASSWORD=$db_pass" >> .env
echo "ROOT_PASSWORD=$root_pass" >> .env
echo "CLIENT_ID=$client_id" >> .env
echo "CLIENT_SECRET=$client_secret" >> .env
echo "API_HOSTNAME=$api_hostname" >> .env
echo "SITE_HOSTNAME=$site_hostname" >> .env
echo "FLASK_SECRET=$flask_secret" >> .env
echo "BOT_TOKEN=$bot_token" >> .env
echo "BOT_OWNER=$bot_owner" >> .env
echo "DEBUG_CHANNEL=$debug_channel" >> .env

echo "Building docker containers..."
docker-compose -f docker-compose-production.yml build
echo "Setting up docker..."
docker-compose -f docker-compose-profuction.yml up -d

echo "Setting up database..."
docker exec partyfiller_backend_1 alembic revision --autogenerate -m "Initial migration."
docker exec partyfiller_backend_1 alembic upgrade head

echo "If you want to use your own Discord bot to handle the discord side remember to run setup there also."