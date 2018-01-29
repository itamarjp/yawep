#!/usr/bin/env python3
import pika
import json
import sys
import os
import time
import backend

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
queue = "domains"
channel.queue_declare(queue = queue)

VirtualHost = """
<VirtualHost *:80>
 DocumentRoot {1}
 ServerAlias www.{0}
 ServerAlias {0}
</VirtualHost>

<VirtualHost *:443>
 DocumentRoot {1}
 ServerName server.{0}
 ServerAlias www.{0}
 ServerAlias {0}
 SSLEngine on
 SSLCertificateFile /etc/letsencrypt/live/{0}/cert.pem
 SSLCertificateKeyFile /etc/letsencrypt/live/{0}/privkey.pem
 SSLCertificateChainFile /etc/letsencrypt/live/{0}/fullchain.pem
</VirtualHost>


<Directory {1}/>
 AddDefaultCharset UTF-8
 Require all granted
 Options +FollowSymLinks +Indexes
</Directory>

"""

home = "/var/www/domains/{}/htdocs"
apache_conf = "/etc/httpd/conf.d/{}.conf"

def callback(ch, method, properties, body):
 print(" [x] DM Received %r" % body)
 temp = body.replace(b"'" ,  b'"').decode("utf-8") 
 x = json.loads(temp)
 #print (type(x))
 domain_name =  x['name']
 action = x['action']
 homedir = home.format(domain_name)
 conf_d = apache_conf.format(domain_name)
 virtualhost = VirtualHost.format(domain_name , homedir)

 if action == "new":
  backend.make_web_home(homedir)
  file = open(conf_d,"w")
  file.write(virtualhost)
  file.close()
  print("Getting a LetEncrypt certificate for ", domain_name)
  os.system("service httpd stop")
  os.system("certbot certonly --standalone --preferred-challenges http -d {} -m itamar@ispbrasil.com.br  --agree-tos -n".format(domain_name))

 if action == "delete":
  print("Removing domain", domain_name)
  try:
   print("Removing apache config file", conf_d)
   os.unlink(conf_d)
  except:
   pass
  backend.remove_web_home(homedir[:-7])
 os.system("service httpd restart")
 time.sleep(10)


channel.basic_consume(callback , queue = queue , no_ack = True)

print("[*] Waiting for messages on queue {}. To exit press CTRL+C".format(queue))
try:
 channel.start_consuming()
except KeyboardInterrupt:
 print("Closing")
 channel.close()
 connection.close()


