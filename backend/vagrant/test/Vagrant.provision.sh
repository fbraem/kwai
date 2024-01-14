#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive

VAGRANT_HOME="/home/vagrant"

KWAI_DATABASE_NAME=$1
KWAI_DATABASE_USER=$2
KWAI_DATABASE_PASSWORD=$3
KWAI_RABBITMQ_VHOST=$4
KWAI_RABBITMQ_USER=$5
KWAI_RABBITMQ_PASSWORD=$6
KWAI_EMAIL_HOST=$7
KWAI_EMAIL_PORT=$8
KWAI_EMAIL_USER=$9
KWAI_EMAIL_PASSWORD=${10}
KWAI_JWT_SECRET=${11}
KWAI_REDIS_PASSWORD=${12}

KWAI_TOML_FILE=$VAGRANT_HOME/.kwai.toml
PROFILE=$(cat <<EOF
export DATABASE_URL=mysql://$KWAI_DATABASE_USER:$KWAI_DATABASE_PASSWORD@localhost/$KWAI_DATABASE_NAME
export KWAI_SETTINGS_FILE=$KWAI_TOML_FILE
EOF
)
echo "$PROFILE" >> "$VAGRANT_HOME/.profile"

apt-get update

# Python
apt-get install python3-pip -y
pip --version
su -c "pip install poetry" vagrant

# MySQL
debconf-set-selections <<< "mysql-server mysql-server/root_password password $KWAI_DATABASE_PASSWORD"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $KWAI_DATABASE_PASSWORD"
apt-get install -y mysql-server

MYSQL_SETUP=$(cat <<EOF
DROP DATABASE IF EXISTS $KWAI_DATABASE_NAME;
CREATE DATABASE $KWAI_DATABASE_NAME;
DROP USER IF EXISTS '$KWAI_DATABASE_USER'@'%';
CREATE USER '$KWAI_DATABASE_USER'@'%' IDENTIFIED BY '$KWAI_DATABASE_PASSWORD';
GRANT ALL PRIVILEGES ON *.* TO '$KWAI_DATABASE_USER'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF
)
echo "$MYSQL_SETUP" > "$VAGRANT_HOME/mysql_setup.sql"

# install dbmate
sudo curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64
sudo chmod +x /usr/local/bin/dbmate

# Redis
apt-get install redis-server -y
REDIS_CONFIG=$(cat <<EOF
port 6379
daemonize yes
save 60 1
bind 0.0.0.0
tcp-keepalive 300
dbfilename dump.rdb
dir /var/lib/redis
rdbcompression yes
requirepass ${KWAI_REDIS_PASSWORD}
EOF
)
echo "${REDIS_CONFIG}" > /etc/redis/redis.conf
sudo /etc/init.d/redis-server restart

# Generate .kwai.toml
KWAI_TOML=$(cat << EOF
[security]
jwt_secret="$KWAI_JWT_SECRET"
jwt_refresh_secret="$KWAI_JWT_SECRET"
[template]
path="$VAGRANT_HOME/kwai/backend/templates"
[db]
host="localhost"
name="$KWAI_DATABASE_NAME"
user="$KWAI_DATABASE_USER"
password="$KWAI_DATABASE_PASSWORD"
[website]
url="http://localhost"
email="franky.braem@gmail.com"
name="Kwai Website"
[email]
host="$KWAI_EMAIL_HOST"
user="$KWAI_EMAIL_USER"
password="$KWAI_EMAIL_PASSWORD"
port=$KWAI_EMAIL_PORT
ssl=false
tls=true
from="franky.braem@gmail.com"
[redis]
host="127.0.0.1"
password="$KWAI_REDIS_PASSWORD"
EOF
)
echo "$KWAI_TOML" > $KWAI_TOML_FILE
chown vagrant:vagrant $KWAI_TOML_FILE

# Generate the test script
TEST_SCRIPT=$(cat <<EOF
#!/bin/bash

# Clone the git repository
rm -rf kwai
git clone https://codeberg.org/zumuta/kwai.git
cd kwai/backend/src
poetry install --with dev,docs

# Drop/create the database
mysql -uroot -p"$KWAI_DATABASE_PASSWORD" < "$VAGRANT_HOME/mysql_setup.sql"

# Migrate database
export DBMATE_MIGRATIONS_DIR="$VAGRANT_HOME/kwai/backend/migrations"
export DBMATE_NO_DUMP_SCHEMA="true"
export DBMATE_WAIT="true"
export DBMATE_WAIT_TIMEOUT="30s"
dbmate up

# Run the tests
poetry run pytest --cov=kwai --cov-report html
if [ $? -ne 0 ]; then
  echo "One or more tests failed."
  exit 1
fi
poetry run coverage-badge -o ./htmlcov/coverage.svg
rm -rf /kwai_sync/backend/docs/tests/coverage/*
cp -R ./htmlcov/* /kwai_sync/backend/docs/tests/coverage
EOF
)
echo "$TEST_SCRIPT" > "$VAGRANT_HOME/kwai_test.sh"
chown vagrant:vagrant "$VAGRANT_HOME/kwai_test.sh"
chmod u+x "$VAGRANT_HOME/kwai_test.sh"
