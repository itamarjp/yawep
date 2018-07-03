#!/usr/bin/python3

import pymysql.cursors #https://github.com/PyMySQL/PyMySQL
import string


def runsql(sql, cursor):
 print("sql: {}".format(sql))
 try:
   cursor.execute(sql)
 except (pymysql.err.ProgrammingError,pymysql.err.OperationalError,pymysql.err.InternalError) as e:
   print ("DB Error: {}".format(e))



alphabet = string.ascii_letters + string.digits
try:
 import secrets
 password = ''.join(secrets.choice(alphabet) for i in range(30)) # for a 20-character password
except ImportError:
 from os import urandom
 password =  "".join(alphabet[ord(c) % len(alphabet)] for c in urandom(30))

file = open("/root/.mysql_password","w")
file.write(password)
file.close()


try:
     cnx = pymysql.connect(user='root',host='127.0.0.1', db='mysql')
except pymysql.err.OperationalError as e:
     print ("DB Error: {}".format(e))

cursor = cnx.cursor()

query =  ("delete from user where user=''")
runsql(query,cursor)

query =  ("delete from user where host in ('::1', 'localhost.localdomain', 'localhost')")
runsql(query,cursor)

query =  ("update user set password = password('{}') ,  host='%' where user='root'".format(password))
runsql(query,cursor)

query =  ("delete from user where password=''")
runsql(query,cursor)

query =  ("flush privileges")
runsql(query,cursor)

query = ("SHUTDOWN")
runsql(query,cursor)

cursor.close()

cnx.close()




