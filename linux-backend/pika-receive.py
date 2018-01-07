#!/usr/bin/env python
import pika
import json
import mysql.connector


file = open("/root/.mysql_password","r")
mysql_password = file.readline()
file.close()


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='databases')
channel.queue_declare(queue='domains')

def runsql(sql, cursor):
 print("executing sql:\n {}".format(sql))
 try:
  cursor.execute(sql)
 except mysql.connector.Error as err:
  print(err)
  print("falhou:")
  print(sql)



def callback_domains(ch, method, properties, body):
    print(" [x] DM Received %r" % body)

def callback_databases(ch, method, properties, body):
    print(" [x] DB Received %r" % body)
    temp = body.replace("'", "\"")
    x = json.loads(temp)
    #print (type(x))
    username =  x['username']
    password =  x['password']
    databasename = x['databasename']
    action = x['action']
    try:
      cnx = mysql.connector.connect(user='root',host='127.0.0.1', password = mysql_password, database='mysql')

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
       print(err)

    cursor = cnx.cursor()
    if action == "new":
     query =  "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(databasename)
     runsql(query,cursor)
     query = "GRANT ALL ON {}.* TO {} IDENTIFIED BY '{}'".format(databasename, username, password)
     runsql(query,cursor)
    if action == "delete":
     query =  ("DROP DATABASE {}".format(databasename))
     runsql(query,cursor)
     query =  ("DROP USER {}".format(username))
     runsql(query,cursor)
    cursor.close()
    cnx.close()

channel.basic_consume(callback_databases,queue='databases', no_ack=True)
channel.basic_consume(callback_domains,queue='domains', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()



