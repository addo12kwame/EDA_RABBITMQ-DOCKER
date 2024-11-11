import json,os,pika
import time
from main import Product,db,app
from producer import channel


def callback(ch,method,properties,body):
    print('Received in main')
    data = json.loads(body)
    print(data)
    with app.app_context():
        if properties.content_type == "product_created":
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print('product created')
        elif properties.content_type == "product_updated":
            product = db.session.get(Product,(data['id']))
            if product:
                product.title = data.get('title')
                product.image = data.get('image')
                db.session.commit()
                print('product updated')

        elif properties.content_type == "product_deleted":
            product = db.session.get(Product,data)  #  Since we are sending the pk as a string not a object from django
            db.session.delete(product)
            db.session.commit()
            print('product deleted')


channel = None
retries = 5
while retries > 0:
    try:

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal', port=8090))

        channel = connection.channel()
        channel.queue_declare(queue="myqueue")
        channel.basic_consume(queue='myqueue', on_message_callback=callback, auto_ack=True)

        print("Started Consuming")
        if retries < 5 :
            retries = 5
            print("Resetting retries")
        channel.start_consuming()
    except Exception:
        print(f"Retries left {retries}")
        time.sleep(5)
        retries-=1
channel.close()