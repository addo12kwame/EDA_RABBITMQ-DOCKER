import json,os,pika
from dotenv import load_dotenv

load_dotenv(".env")


params = pika.URLParameters(os.getenv("API_KEY_RABBITMQ"))

connection  = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method,body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='',routing_key='main', body=json.dumps(body), properties=properties)
