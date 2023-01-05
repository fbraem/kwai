#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive

KWAI_DATABASE_NAME=$1
KWAI_DATABASE_USER=$2
KWAI_DATABASE_PASSWORD=$3
KWAI_RABBITMQ_USER=$4
KWAI_RABBITMQ_PASSWORD=$5

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

# update mysql conf file to allow remote access to the db
sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf
service mysql restart

# Install RabbitMQ

apt-get install curl gnupg apt-transport-https -y

curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null
curl -1sLf "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xf77f1eda57ebb1cc" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg > /dev/null
curl -1sLf "https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/io.packagecloud.rabbitmq.gpg > /dev/null

RABBITMQ_LIST=$(cat <<EOF
deb [signed-by=/usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg] http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu jammy main
deb-src [signed-by=/usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg] http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu jammy main
deb [signed-by=/usr/share/keyrings/io.packagecloud.rabbitmq.gpg] https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ jammy main
deb-src [signed-by=/usr/share/keyrings/io.packagecloud.rabbitmq.gpg] https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu/ jammy main
EOF
)
echo "${RABBITMQ_LIST}" > /etc/apt/sources.list.d/rabbitmq.list

apt-get update -y
apt-get install -y erlang-base \
    erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
    erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
    erlang-runtime-tools erlang-snmp erlang-ssl \
    erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl
apt-get install rabbitmq-server -y --fix-missing

rabbitmq-plugins enable rabbitmq_management
echo "$KWAI_RABBITMQ_PASSWORD" | rabbitmqctl add_user "$KWAI_RABBITMQ_USER"
rabbitmqctl add_vhost kwai
rabbitmqctl set_permissions -p "kwai" "$KWAI_RABBITMQ_USER" ".*" ".*" ".*"
