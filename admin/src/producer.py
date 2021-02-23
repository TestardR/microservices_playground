import pika

params = pika.ConnectionParameters('host.docker.internal')
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish():
    channel.basic_publish(exchange='', routing_key='main', body='hello')
