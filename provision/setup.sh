#!/bin/bash

echo "Provisionamento da VM django + postgresql"

echo "Atualizado apt-get"
apt-get update > /dev/null
apt-get upgrade > /dev/null

echo "Instalando virtualenv"
apt-get install -y virtualenv  > /dev/null

echo "Instalando git"
apt-get install -y git > /dev/null

echo "Instalando Python3"
apt-get -y install python3-pip python3-dev libpq-dev python3-virtualenv python3-setuptools  > /dev/null

echo "Instalando postgresql"
apt-get install -y postgresql postgresql-contrib > /dev/null

echo "Instalando virtualenv"
apt-get install -y virtualenv > /dev/null

echo "Configurando Virtualenv e Django"
cd /vagrant
virtualenv -p python3 .venv
source .venv/bin/activate

pip install django psycopg2  > /dev/null
pip freeze > requirements.txt

deactivate

echo "Configurando postgresql"
sudo -u postgres psql -c "CREATE USER pmoc WITH PASSWORD 'pmoc';" > /dev/null
sudo -u postgres psql -c "CREATE DATABASE pmoc;" > /dev/null
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE pmoc to pmoc;" > /dev/null

echo "Instalação completa"
