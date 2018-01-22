#!/usr/bin/env python3
import requests
import json
import time

url = 'http://painel.ispbrasil.com.br:5000/api/domains'
while True:
 r = requests.get(url, auth=('x', 'x'))
 print(r.status_code)
 if (r.status_code < 400):
  for x in r.json():
    print ("removing", x['id'],"domain = " ,x['name'])
    x = requests.delete("%s/%s" % (url,x['id']), auth=('x', 'x'))
    #for key in x.keys(): print(key)

 print ("Adding a new domain")
 y = requests.post(url, json = {"user_id":"1" , "name":"test1.ispbrasil.com.br"}, auth=('x', 'x'))
 time.sleep(10)