import os
import sys
import json
import logging

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'media_core.settings')
# django.setup()

import pika
from django.conf import settings
import tasks

logger = logging.getLogger(__name__)

def process_thumbnail_queue(ch, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    logger.info(message)
    tasks.generate_thumbnail.delay(message.get("bucket"), message.get("filename"), "thumbnails", (128, 128))

def process_other_queue(ch, method, properties, body):
    message = body.decode('utf-8')
    # Process messages from the other queue
    logger.info(f"Processing message from other_queue: {message}")

# Establish connection to RabbitMQ
credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, credentials=credentials, virtual_host=settings.RABBITMQ_VHOST))
channel = connection.channel()

# # Declare exchanges
# channel.exchange_declare(exchange='thumbnail_exchange', exchange_type='direct')
# channel.exchange_declare(exchange='other_exchange', exchange_type='direct')

# Declare queues
channel.queue_declare(queue='image_processing_queue')
channel.queue_declare(queue='other_queue')

# # Bind queues to exchanges
# channel.queue_bind(exchange='thumbnail_exchange', queue='thumbnail_queue', routing_key='thumbnail_key')
# channel.queue_bind(exchange='other_exchange', queue='other_queue', routing_key='other_key')

# Set up consumers for each queue
channel.basic_consume(queue='image_processing_queue', on_message_callback=process_thumbnail_queue, auto_ack=True)
channel.basic_consume(queue='other_queue', on_message_callback=process_other_queue, auto_ack=True)

logger.info('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()