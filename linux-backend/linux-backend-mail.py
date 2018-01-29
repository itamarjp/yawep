#!/usr/bin/env python3
import pika
import json
import sys
import os
from pwd import getpwnam
import time
import shutil
import crypt
import tempfile


x = "/var/mail/vhosts/ispbrasil.com.br/itamar"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
queue = "emails"
channel.queue_declare(queue = queue)

virtual_domains = "/etc/postfix/virtual_domains"
def add_domain(domain_name):
  print("adding domain {} to postfix".format(domain_name))
  file1 = open(virtual_domains)
  file2 = open(virtual_domains, "a")
  found = 0
  for line in file1:
    if (line == domain_name):
     found = 1
     break
  if (found == 0):
    file2.write("{}\n".format(domain_name))
  file1.close()
  file2.close()

def remove_domain(domain_name):
  print("Removing domain {} from postfix".format(domain_name))
  file1 = open(virtual_domains)
  file2 = tempfile.NamedTemporaryFile(delete=False)
  for line in file1:
    if (line != domain_name):
     file2.write(line)
  file1.close()
  file2.close()
  shutil.move(file2.name, virtual_domains)




def callback(ch, method, properties, body):
 print(" [x] DF Received %r" % body)
 temp = body.replace(b"'" ,  b'"').decode("utf-8") 
 x = json.loads(temp)
 username = x['username']
 password = x['password']
 domain_name =  x['domain_name']
 hashed_password = crypt.crypt(password)
 action = x['action']
 if action == "new":
  add_domain(domain_name)

 if action == "delete":
  remove_domain(domain_name)

 os.system("service postfix restart")
 time.sleep(10)


channel.basic_consume(callback , queue = queue , no_ack=True)

print("[*] Waiting for messages on queue {}. To exit press CTRL+C".format(queue))
try:
 channel.start_consuming()
except KeyboardInterrupt:
 print("Closing")
 channel.close()
 connection.close()


