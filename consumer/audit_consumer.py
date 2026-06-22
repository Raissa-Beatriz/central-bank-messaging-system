import json
import os
import pika
from pika import PlainCredentials
from datetime import datetime
from shared.config import (
    RABBITMQ_HOST,
    RABBITMQ_QUEUE,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    AUDIT_LOG_PATH
)

def ensure_log_dir():
    os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)

def format_log_entry(transaction):
    dt = datetime.fromisoformat(transaction["timestamp"])
    timestamp_fmt = dt.strftime("%Y-%m-%d %H:%M:%S")

    return (
        f"[{timestamp_fmt}] "
        f"{transaction['transactionId']} | "
        f"{transaction['senderBank']} | "
        f"{transaction['receiverBank']} | "
        f"{transaction['amount']:.2f}\n"
    )

def callback(ch, method, properties, body):
    transaction = json.loads(body.decode("utf-8"))
    log_entry = format_log_entry(transaction)

    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as file:
        file.write(log_entry)

    print(f"[AUDIT] Registrado: {log_entry.strip()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    ensure_log_dir()

    credentials = PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        auto_ack=False
    )

    print("[*] Audit Logging Service aguardando mensagens...")
    channel.start_consuming()

if __name__ == "__main__":
    main()