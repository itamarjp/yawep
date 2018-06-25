#!/usr/bin/bash

sed -i -e 's/local   all             all                                     trust/local   all             all                                     md5/' /var/lib/pgsql/data/pg_hba.conf
sed -i -e 's/host    all             all             127.0.0.1/32            trust/host   all             all             127.0.0.1/32             md5/' /var/lib/pgsql/data/pg_hba.conf
sed -i -e 's/host    all             all             ::1/128                 trust/host    all             all             ::1/128                 md5/' /var/lib/pgsql/data/pg_hba.conf

service postregsql  restart
