import json,os,django,pika,time


######################################################################################
os.environ.setdefault("DJANGO_SETTINGS_MODULE","admin.settings")          #
django.setup()                                                                      #
                                                                                   #
from products.models import Products                                              #
################################################################################ #
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal', port=8090))
        break
    except pika.exceptions.AMQPConnectionError:
        print("Consumer: Waiting for RabbitMQ...")
        time.sleep(5)

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