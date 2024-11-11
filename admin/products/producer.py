import json,os,pika,time

def publish(method,body):
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal', port=8090))
            break
        except pika.exceptions.AMQPConnectionError:
            print("Consumer: Waiting for RabbitMQ...")
            time.sleep(5)

    channel = connection.channel()

    channel.queue_declare(queue="myqueue")
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='',routing_key='myqueue', body=json.dumps(body), properties=properties)

