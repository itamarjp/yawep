#!/usr/bin/env python
import sys
import pika

queue = sys.argv[1]
msg = sys.argv[2]

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=queue)

channel.basic_publish(exchange='',routing_key=queue, body='Hello World! {0}'.format(msg) )
print(" [x] Sent {} to {}'".format(msg,queue))

connection.close()

