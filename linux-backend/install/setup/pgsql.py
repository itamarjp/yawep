#!/usr/bin/env python3

import pg8000
import string

alphabet = string.ascii_letters + string.digits
try:
 import secrets
 password = ''.join(secrets.choice(alphabet) for i in range(30)) # for a 20-character password
except ImportError:
 from os import urandom
 password =  "".join(alphabet[ord(c) % len(alphabet)] for c in urandom(30))

file = open("/root/.pgsql_password","w")
file.write(password)
file.close()

try:
  cnx = pg8000.connect(user="postgres")
except:
    print('error in pgsql module')

cursor = cnx.cursor()

query =  ("ALTER ROLE postgres WITH PASSWORD '{}';".format(password))
print(query)
cursor.execute(query)


cursor.close()

cnx.close()
