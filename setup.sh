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
echo -e "DATABASE=$database\n" | tee -a .env
echo -e "DB_USER=$db_user\n" | tee -a .env
echo -e "DB_PASSWORD=$db_pass\n" | tee -a .env
echo -e "ROOT_PASSWORD=$root_pass\n" | tee -a .env
echo -e "CLIENT_ID=$client_id\n" | tee -a .env
echo -e "CLIENT_SECRET=$client_secret\n" | tee -a .env
echo -e "API_HOSTNAME=$api_hostname\n" | tee -a .env
echo -e "SITE_HOSTNAME=$site_hostname\n" | tee -a .env
echo -e "FLASK_SECRET=$flask_secret\n" | tee -a .env
echo -e "BOT_TOKEN=$bot_token\n" | tee -a .env
echo -e "BOT_OWNER=$bot_owner\n" | tee -a .env
echo -e "DEBUG_CHANNEL=$debug_channel\n" | tee -a .env
echo -e "WEBHOOK_ID=" | tee -a .env

echo "Building docker containers..."
docker-compose -f docker-compose-production.yml build
echo "Setting up docker..."
docker-compose -f docker-compose-profuction.yml up -d

echo "Setting up database..."
docker exec partyfiller_backend_1 flask db init
docker exec partyfiller_backend_1 flask db migrate -m "Initial migration."
docker exec partyfiller_backend_1 flask db upgrade

echo "If you want to use your own Discord bot to handle the discord side remember to run setup there also."