#!/usr/bin/bash

service httpd stop
certbot certonly --standalone --preferred-challenges http -d painel.ispbrasil.com.br -m itamar@ispbrasil.com.br  --agree-tos -n

sed -i -e 's/SSLCertificateFile .*/SSLCertificateFile \/etc\/letsencrypt\/live\/painel.ispbrasil.com.br\/cert.pem/' /etc/httpd/conf.d/ssl.conf
sed -i -e 's/SSLCertificateKeyFile .*/SSLCertificateKeyFile \/etc\/letsencrypt\/live\/painel.ispbrasil.com.br\/privkey.pem/' /etc/httpd/conf.d/ssl.conf

service httpd start