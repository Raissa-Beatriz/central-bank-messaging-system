import json
import random
import uuid
from datetime import datetime

def generate_transaction(sender_bank, receiver_bank):
    return {
        "transactionId": f"TX-{uuid.uuid4().hex[:10].upper()}",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "senderBank": sender_bank,
        "receiverBank": receiver_bank,
        "senderAccount": str(random.randint(10000, 99999)),
        "receiverAccount": str(random.randint(10000, 99999)),
        "amount": round(random.uniform(10, 5000), 2)
    }

def transaction_to_json(transaction):
    return json.dumps(transaction, ensure_ascii=False)