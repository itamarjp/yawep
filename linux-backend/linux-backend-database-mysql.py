#!/usr/bin/env python3
import pika
import json
import pymysql.cursors #https://github.com/PyMySQL/PyMySQL

file = open("/root/.mysql_password","r")
mysql_password = file.readline()
file.close()


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
queue = "databases"
channel.queue_declare(queue = queue)

def runsql(sql, cursor):
 print("sql: {}".format(sql))
 try:
   cursor.execute(sql)
 except (pymysql.err.ProgrammingError,pymysql.err.OperationalError,pymysql.err.InternalError) as e:
   print ("DB Error: {}".format(e))

def callback(ch, method, properties, body):
    print(" [x] DB Received: %s" % body)
    temp = body.replace(b"'" ,  b'"').decode("utf-8")
    try:
        x = json.loads(temp)
    except:
       print ("erro no json: {}".format(temp))
       return
    #print (type(x))
    username =  x['username']
    password =  x['password']
    databasename = x['databasename']
    action = x['action']
    try:
     cnx = pymysql.connect(user='root',host='127.0.0.1', passwd = mysql_password, db='mysql')
    except pymysql.err.OperationalError as e:
     print ("DB Error: {}".format(e))
     return

    cursor = cnx.cursor()
    
    if action == "new" or action =="edit":
     query =  "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(databasename)
     runsql(query,cursor)
     query =  ("DROP USER {}".format(username))
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

channel.basic_consume(callback , queue = queue , no_ack=True)

print("[*] Waiting for messages on queue {}. To exit press CTRL+C".format(queue))
try:
 channel.start_consuming()
except KeyboardInterrupt:
 print("Closing")
 channel.close()
 connection.close()
