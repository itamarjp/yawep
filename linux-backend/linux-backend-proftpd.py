#!/usr/bin/env python3
import pika
import json
import sys
import os
from pwd import getpwnam
import time
import shutil

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='ftpaccounts')

proftp_conf = "/etc/passwd.ftp"

def callback(ch, method, properties, body):
 print(" [x] DF Received %r" % body)
 temp = body.replace(b"'" ,  b'"').decode("utf-8") 
 x = json.loads(temp)
 #print (type(x))
 domain_name =  x['domain_name']
 print(domain_name)
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
  print("Removing directory : " , homedir[:-7])
  shutil.rmtree(homedir[:-7] , ignore_errors=True)

 os.system("service httpd restart")
 time.sleep(10)


channel.basic_consume(callback , queue='domains', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()



