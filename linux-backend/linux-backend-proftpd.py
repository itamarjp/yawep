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


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='ftpaccounts')

passwd_ftp = "/etc/passwd.ftp"

def add_ftp(username, password, domain_name ):
  hashed_password = crypt.crypt(password)
  nome = "ftp-user-{}".format(domain_name)
  home = "/var/www/domains/{}/htdocs".format(domain_name)
  password_line = "{}:{}:14:50:{}:{}:/sbin/nologin\n".format(username, hashed_password, nome , home)
  file1 = open(passwd_ftp)
  file2 = tempfile.NamedTemporaryFile(delete=False)
  for line in file1:
    (user_name, hashed_password , uid, gid, gecos, homedir, usershell) = line1.split(':')
        file2.write(line)
  file2.write(password_line.encode('utf-8'))
  file1.close
  file2.close()
  shutil.move(file2.name, passwd_ftp)

def remove_ftp(username):
  print("Removing username {} from FTP".format(usernamename))
  file1 = open(passwd_ftp)
  file2 = tempfile.NamedTemporaryFile(delete=False)
  for line in file1:
    (user_name, hashed_password , uid, gid, gecos, homedir, usershell) = line1.split(':')
    if (username != user_name):
     file2.write(line)
  file1.close()
  file2.close()
  shutil.move(file2.name, passwd_ftp)




def callback(ch, method, properties, body):
 print(" [x] DF Received %r" % body)
 temp = body.replace(b"'" ,  b'"').decode("utf-8") 
 x = json.loads(temp)
 username = x['username']
 password = x['password']
 domain_name =  x['domain_name']
 action = x['action']
 
 if action == "new":
  add_ftp(username, password, domain_name)
 if action == "delete":
  remove_ftp(username)

 os.system("service proftpd restart")
 time.sleep(10)


channel.basic_consume(callback , queue='ftpaccounts', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
try:
 channel.start_consuming()
except KeyboardInterrupt:
 print("Closing")
 channel.close()
 connection.close()


