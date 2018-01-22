#!/usr/bin/env python3
import pika
import json
import MySQLdb


file = open("/root/.mysql_password","r")
mysql_password = file.readline()
file.close()


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='databases')

def runsql(sql, cursor):
 print("executing sql:\n {}".format(sql))
 try:
  cursor.execute(sql)
 except _mysql.Error as e:
  print ("Error %d: %s" % (e.args[0], e.args[1]))
  print("falhou:")
  print(sql)


def callback(ch, method, properties, body):
    print(" [x] DB Received %r" % body)
    temp = body.replace("'", "\"")
    x = json.loads(temp)
    #print (type(x))
    username =  x['username']
    password =  x['password']
    databasename = x['databasename']
    action = x['action']
    try:
      cnx = MySQLdb.connect(user='root',host='127.0.0.1', password = mysql_password, database='mysql')
    except _mysql.Error as e:
     print ("Error %d: %s" % (e.args[0], e.args[1]))

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

channel.basic_consume(callback , queue='databases', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()



