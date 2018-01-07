#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

for i in range(100000):
  channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World! {0}'.format(i) )
  print(" [x] Sent 'Hello World! {0}'".format(i))

connection.close()

