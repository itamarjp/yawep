#!/usr/bin/env python3
import requests
import json
import time

url = 'http://painel.ispbrasil.com.br:5000/api/databases'
while True:
 r = requests.get(url, auth=('x', 'x'))
 print(r.status_code)
 if (r.status_code < 400):
  for x in r.json():
    print ("removing", x['id'],"databasename = " ,x['databasename'])
    x = requests.delete("%s/%s" % (url,x['id']), auth=('x', 'x'))
    #for key in x.keys(): print(key)

 print ("Adding a new database")
 y = requests.post(url, json = {"domain_id":"1" , "databasename":"x", "username": "x", "password":"x"}, auth=('x', 'x'))
 time.sleep(10)