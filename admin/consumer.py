import json,os,django,pika
from dotenv import load_dotenv

load_dotenv(".env")



#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE","admin.settings")
# django.setup()

# from products.models import Products
print(os.getenv("API_KEY_RABBITMQ"))

params = pika.URLParameters(os.getenv("API_KEY_RABBITMQ"))
connection  = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="admin")

def callback(ch,method,properties,body):
    print('Received in admin')
    id = json.loads(body)
    print(f'User id ->{id}')
    product = Products.objects.get(id=id)
    if product:
        product.likes += 1
        product.save()
        print(f"Product likes increased to {product.likes}")

channel.basic_consume(queue='admin',on_message_callback=callback,auto_ack=True)

print("Started Consuming")
channel.start_consuming()
channel.close()