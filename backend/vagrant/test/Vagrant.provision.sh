#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive

KWAI_DATABASE_NAME=$1
KWAI_DATABASE_USER=$2
KWAI_DATABASE_PASSWORD=$3
KWAI_REDIS_PASSWORD=$4

apt-get update

# Python


# MySQL
debconf-set-selections <<< "mysql-server mysql-server/root_password password $KWAI_DATABASE_PASSWORD"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $KWAI_DATABASE_PASSWORD"
apt-get install -y mysql-server

MYSQL_SETUP=$(cat <<EOF
CREATE DATABASE $KWAI_DATABASE_NAME;
CREATE USER '$KWAI_DATABASE_USER'@'%' IDENTIFIED BY '$KWAI_DATABASE_PASSWORD';
GRANT ALL PRIVILEGES ON *.* TO '$KWAI_DATABASE_USER'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF
)
echo "${MYSQL_SETUP}" > /var/tmp/mysql_setup.sql
mysql -uroot -p"$KWAI_DATABASE_PASSWORD" < /var/tmp/mysql_setup.sql

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
