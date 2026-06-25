import time
import pika
from pika import PlainCredentials
from shared.config import RABBITMQ_HOST, RABBITMQ_QUEUE, RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_EXCHANGE, RABBITMQ_ROUTING_KEY
from shared.utils import generate_transaction, transaction_to_json

BANK_NAME = "BankC"
TARGET_BANK = "BankA"

def main():
    credentials = PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type="direct", durable=True)
    channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE, routing_key=RABBITMQ_ROUTING_KEY)

    while True:
        transaction = generate_transaction(BANK_NAME, TARGET_BANK)
        message = transaction_to_json(transaction)

        channel.basic_publish(
            exchange=RABBITMQ_EXCHANGE,
            routing_key=RABBITMQ_ROUTING_KEY,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )

        print(f"[{BANK_NAME}] Enviou: {message}")
        time.sleep(4)

if __name__ == "__main__":
    main()