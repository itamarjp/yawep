#!/usr/bin/env python3
import sys
import pika

if (len(sys.argv) < 3 ):
 print("usage:\n","./pika-send.py domains test-message")
 sys.exit(1)
queue = sys.argv[0]
msg = sys.argv[1]



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=queue)

channel.basic_publish(exchange='',routing_key=queue, body='Hello World! {0}'.format(msg) )
print(" [x] Sent {} to {}'".format(msg,queue))

connection.close()

