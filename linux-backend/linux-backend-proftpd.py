#!/usr/bin/env python3
import pika
import json
import sys
import os
import time
import shutil
import crypt
import tempfile
import backend


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
queue = "ftpaccounts"
channel.queue_declare(queue = queue)

passwd_ftp = "/etc/passwd.ftp"

def add_ftp(username, password, domain_name ):
  hashed_password = crypt.crypt(password)
  nome = "ftp-user-{}".format(domain_name)
  home = "/var/www/domains/{}/htdocs".format(domain_name)
  backend.make_home(home)
  password_line = "{}:{}:14:50:{}:{}:/sbin/nologin\n".format(username, hashed_password, nome , home)
  file1 = open(passwd_ftp)
  file2 = tempfile.NamedTemporaryFile(delete=False)
  for line in file1:
    (user_name, hashed_password , uid, gid, gecos, homedir, usershell) = line.split(':')
    print("debug {}, {}".format(username, user_name))
    if (username != user_name):
     file2.write(line.encode('utf-8'))
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
 try:
  username = x['username']
  password = x['password']
  domain_name =  x['domain_name']
  action = x['action']
 except KeyError:
  print("missing data in the msg")

 if action == "new":
  add_ftp(username, password, domain_name)
 if action == "delete":
  remove_ftp(username)

 os.system("service proftpd restart")
 time.sleep(10)


channel.basic_consume(callback , queue = queue , no_ack=True)

print("[*] Waiting for messages on queue {}. To exit press CTRL+C".format(queue))
try:
 channel.start_consuming()
except KeyboardInterrupt:
 print("Closing")
 channel.close()
 connection.close()


