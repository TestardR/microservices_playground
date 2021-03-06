import pika

params = pika.ConnectionParameters('host.docker.internal')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(cb, method, properties, body):
    print('Received in admin')


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
