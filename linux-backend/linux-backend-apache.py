#!/usr/bin/env python
import pika
import json
import sys
import os
from pwd import getpwnam
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='domains')

VirtualHost = """
<VirtualHost *:80>
 DocumentRoot {1}
 ServerName server.{0}
 ServerAlias www.{0}
 ServerAlias {0}
</VirtualHost>
<Directory {1}/>
 AddDefaultCharset UTF-8
 Require all granted
</Directory>
"""
home = "/var/www/domains/{}/htdocs"
apache_conf = "/etc/httpd/conf.d/{}.conf"

def callback(ch, method, properties, body):
 print(" [x] DM Received %r" % body)
 temp = body.replace("'", "\"")
 x = json.loads(temp)
 #print (type(x))
 domain_name =  x['name']
 action = x['action']
 homedir = home.format(domain_name)
 conf_d = apache_conf.format(domain_name)
 virtualhost = VirtualHost.format(domain_name , homedir)

 if action == "new":
  try:
   os.makedirs(homedir)
  except:
   pass
  file = open(conf_d,"w")
  file.write(virtualhost)
  file.close()
  os.chown(homedir, getpwnam('ftp').pw_uid, getpwnam('apache').pw_gid)
  os.system("service httpd restart")
  time.sleep(10)
 if action == "delete":
  #sys.exit(0)
  pass


channel.basic_consume(callback , queue='domains', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()



