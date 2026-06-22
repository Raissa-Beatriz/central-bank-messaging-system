import time
import pika
from pika import PlainCredentials
from shared.config import RABBITMQ_HOST, RABBITMQ_QUEUE, RABBITMQ_USER, RABBITMQ_PASSWORD
from shared.utils import generate_transaction, transaction_to_json

BANK_NAME = "BankA"
TARGET_BANK = "BankB"

def main():
    credentials = PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    while True:
        transaction = generate_transaction(BANK_NAME, TARGET_BANK)
        message = transaction_to_json(transaction)

        channel.basic_publish(
            exchange="",
            routing_key=RABBITMQ_QUEUE,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )

        print(f"[{BANK_NAME}] Enviou: {message}")
        time.sleep(2)

if __name__ == "__main__":
    main()