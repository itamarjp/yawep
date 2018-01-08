#!/usr/bin/env python
import pika
import json
import sys
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
 home = home.format(domain_name)
 print(home)
 sys.exit(0)
 
 if action == "new":
  file = open("/root/.mysql_password","r")
  mysql_password = file.readline()
  file.close()
  exec("mkdir -p $home");
  exec("chown -R ftp:apache $home");
 if action == "delete":
  pass
channel.basic_consume(callback , queue='domains', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()



