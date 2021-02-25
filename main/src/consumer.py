import pika
import json

from src.models import Product
from src.database import SessionLocal

params = pika.ConnectionParameters('host.docker.internal')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')


def callback(cb, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    db = SessionLocal()

    if properties.content_type == 'product_created':
        product = Product(**data)
        db.add(product)
        db.commit()
        db.refresh(product)
        print('Product created')

    elif properties.content_type == 'product_updated':
        product = db.query(Product).get(data['id'])
        product.title = data['title']
        product.image = data['image']
        product.likes = data['likes']
        db.commit()
        db.refresh(product)
        print('Product updated')

    elif properties.content_type == 'product_deleted':
        product = db.query(Product).get(data['id'])
        db.delete(product)
        db.commit()
        print('Product deleted')


channel.basic_consume(
    queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
