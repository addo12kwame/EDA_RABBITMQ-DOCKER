import json,pika,os,time

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal', port=8090))
        break
    except pika.exceptions.AMQPConnectionError:
        print("Producer: Waiting for RabbitMQ...")
        time.sleep(5)

channel = connection.channel()

def publish(method,body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='',routing_key='admin', body=json.dumps(body), properties=properties)
