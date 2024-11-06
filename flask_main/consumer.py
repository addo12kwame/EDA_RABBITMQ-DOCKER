import json,os,pika
from main import Product,db,app
from dotenv import load_dotenv

load_dotenv(".env")

params = pika.URLParameters(os.getenv("API_KEY_RABBITMQ"))
connection  = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="main")

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


channel.basic_consume(queue='main',on_message_callback=callback,auto_ack=True)

print("Started Consuming")
channel.start_consuming()
channel.close()