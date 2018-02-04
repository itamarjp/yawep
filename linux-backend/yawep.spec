Name:           yawep
Version:        0.0.0
Release:        1%{?dist}
Summary:        Yet Another Web Hosting Control Panel


License:        GPLv2+
URL:            https://github.com/itamarjp/yawep
Source0:        yawep.tar.gz

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

%if 0%{?fedora} >= 27
Requires:        python3-virtualenv
Requires:        python3-pika
Requires:        python3-mysql
Requires:        python3-pg8000
Requires:        python3-dns
%endif

%if 0%{?rhel}
Requires:        python34-virtualenv
Requires:        python34-pika
Requires:        python34-mysql
Requires:        python34-pg8000
Requires:        python34-dns
%endif


%description
Yet Another Web Hosting Control Panel

%prep
%autosetup


%build
# % configure
# % make_build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dovecot/
# make _install
touch $RPM_BUILD_ROOT%{_sysconfdir}/dovecot/local.conf

%files
# % license 
%doc linux-backend/readme.txt
%config(noreplace) %{_sysconfdir}/dovecot/local.conf


%changelog
* Sun Feb  4 2018 itamar <itamar@ispbrasil.com.br>
- 
