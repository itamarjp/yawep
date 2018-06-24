#!/usr/bin/bash

/usr/bin/postgresql-setup --initdb --unit postgresql

sed -i -e 's/local   all             all                                     peer/local   all             all                                     trust/' /var/lib/pgsql/data/pg_hba.conf
sed -i -e 's/host    all             all             127.0.0.1/32            ident/host   all             all             127.0.0.1/32             trust/' /var/lib/pgsql/data/pg_hba.conf
sed -i -e 's/host    all             all             ::1/128                 ident/host    all             all             ::1/128                 trust/' /var/lib/pgsql/data/pg_hba.conf

service postregsql  start