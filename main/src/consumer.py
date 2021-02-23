import pika

params = pika.ConnectionParameters('host.docker.internal')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='main')


def callback(cb, method, properties, body):
    print('Received in main')
    print(body)


channel.basic_consume(queue='main', on_message_callback=callback)

print('Started Consuming')

channel.start_consuming()

channel.close()
