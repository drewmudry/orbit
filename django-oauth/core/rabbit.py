import json
import pika
from django.conf import settings

# Default RabbitMQ settings
RABBITMQ_HOST = getattr(settings, 'RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = getattr(settings, 'RABBITMQ_PORT', 5672)
RABBITMQ_USER = getattr(settings, 'RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = getattr(settings, 'RABBITMQ_PASSWORD', 'guest')

def get_rabbitmq_connection():
    """Get a RabbitMQ connection with the configured settings."""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
    )

def publish_to_rabbitmq(routing_key, message):
    """
    Publish a message to RabbitMQ with the given routing key.
    
    Args:
        routing_key (str): The routing key for the message
        message (dict): The message to publish (will be JSON serialized)
    """
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declare the exchange (if it doesn't exist)
        channel.exchange_declare(
            exchange='org_updates',
            exchange_type='topic',
            durable=True
        )
        
        # Declare a queue for each routing key
        queue_name = f"org_updates.{routing_key}"
        channel.queue_declare(queue=queue_name, durable=True)
        
        # Bind the queue to the exchange
        channel.queue_bind(
            exchange='org_updates',
            queue=queue_name,
            routing_key=routing_key
        )
        
        # Publish with persistence
        channel.basic_publish(
            exchange='org_updates',
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Makes messages persistent
            )
        )
        connection.close()
    except Exception as e:
        print(f"Error publishing to RabbitMQ: {e}")