#!/usr/bin/env python3

import MySQLdb
import string

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
  cnx = MySQLdb.connect(user='root',host='127.0.0.1', database='mysql')
except mysql.Error as e:
  print ("Error %d: %s" % (e.args[0], e.args[1]))

cursor = cnx.cursor()

query =  ("delete from user where user=''")
cursor.execute(query)

query =  ("delete from user where host in ('::1', 'localhost.localdomain', 'localhost')")
cursor.execute(query)

query =  ("update user set password = password('{}') ,  host='%' where host='127.0.0.1' and user='root'".format(password))
cursor.execute(query)

query =  ("flush privileges")
cursor.execute(query)

#query = ("SELECT host,user, password from user")
#cursor.execute(query)
#for (host , user, password) in cursor:
#    print("{}, {} {}".format( host, user, password))
cursor.close()

cnx.close()




