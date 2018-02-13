%global         debug_package %{nil}
Name:           yawep
Version:        0.0.0
Release:        1%{?dist}
Summary:        Yet Another Web Hosting Control Panel
License:        GPLv2+
URL:            https://github.com/itamarjp/yawep
Source0:        yawep.tar.gz
BuildArch:      noarch

BuildRequires: systemd
%{?systemd_requires}

Requires:       httpd
Requires:       mod_ssl
Requires:       mod_wsgi
Requires:       phpmyadmin
Requires:       proftpd
Requires:       dovecot
Requires:       postgresql-server
Requires:       php
Requires:       php-fpm
Requires:       php-cli
Requires:       php-pdo
Requires:       php-pgsql
Requires:       php-gd
Requires:       php-xml
Requires:       php-opcache
Requires:       mariadb-server
Requires:       rabbitmq-server
Requires:       certbot
Requires:       python-pika
Requires:       postfix
Requires:       mc
Requires:       net-tools
Requires:       mosh
Requires:       git
Requires:       psmisc
Requires:       ftp
Requires:       roundcubemail
Requires:       screen
Requires:       phpPgAdmin

%if 0%{?fedora} >= 27
Requires:        python3-virtualenv
Requires:        python3-pika
Requires:        python3-PyMySQL
Requires:        python3-pg8000
Requires:        python3-dns
Requires:        python3-flask-admin
Requires:        python3-virtualenv
%endif

%if 0%{?rhel}
Requires:        python34-virtualenv
Requires:        python34-pika
Requires:        python34-pg8000
Requires:        python34-dns
Requires:        python3-PyMySQL
Requires:        python-flask
Requires:        python2-flask
Requires:        python-flask-sqlalchemy
Requires:        python-flask-script
Requires:        python2-flask-migrate
Requires:        python-flask-login
Requires:        python-passlib
Requires:        python2-flask-httpauth
Requires:        python-flask-admin
Requires:        python-virtualenv
%endif


%description
Yet Another Web Hosting Control Panel

%prep
%autosetup


%post
%systemd_post linux-backend-apache.service
%systemd_post linux-backend-database-mysql.service
%systemd_post linux-backend-mail.service
%systemd_post linux-backend-proftpd.service

%preun
%systemd_preun linux-backend-apache.service
%systemd_preun linux-backend-database-mysql.service
%systemd_preun linux-backend-mail.service
%systemd_preun linux-backend-proftpd.service



%postun
%systemd_postun_with_restart linux-backend-apache.service
%systemd_postun_with_restart linux-backend-database-mysql.service
%systemd_postun_with_restart linux-backend-mail.service
%systemd_postun_with_restart linux-backend-proftpd.service

%build

%install

install -Dpm 644 linux-backend/install/setup/local.conf %{buildroot}%{_sysconfdir}/dovecot/local.conf

install -Dpm 644 linux-backend/systemd/linux-backend-apache.service %{buildroot}%{_unitdir}/linux-backend-apache.service
install -Dpm 644 linux-backend/systemd/linux-backend-database-mysql.service %{buildroot}%{_unitdir}/linux-backend-database-mysql.service
install -Dpm 644 linux-backend/systemd/linux-backend-mail.service %{buildroot}%{_unitdir}/linux-backend-mail.service
install -Dpm 644 linux-backend/systemd/linux-backend-proftpd.service %{buildroot}%{_unitdir}/linux-backend-proftpd.service

mkdir -p %{buildroot}%{_datarootdir}/yawep
rm -rf tcc

cp -r . %{buildroot}%{_datarootdir}/yawep


%files
# % license 
%doc linux-backend/readme.txt
%config(noreplace) %{_sysconfdir}/dovecot/local.conf
%{_datarootdir}/yawep/
%ghost %{_datarootdir}/yawep/storage.db
%{_unitdir}/*.service

%changelog
* Sun Feb  4 2018 itamar <itamar@ispbrasil.com.br>
- 
