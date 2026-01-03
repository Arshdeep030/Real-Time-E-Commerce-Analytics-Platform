import json
import time
import random
import uuid
from kafka import KafkaProducer
from datetime import datetime

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_RAW = 'ecommerce_events_raw'

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample data
event_types = ['page_view', 'add_to_cart', 'purchase']
products = ['product_1', 'product_2', 'product_3']
devices = ['mobile', 'desktop', 'tablet']
countries = ['US', 'CA', 'UK']

print("Starting event production to Kafka...")

while True:
    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": f"user_{random.randint(1, 10)}",
        "session_id": f"session_{random.randint(1, 5)}",
        "event_type": random.choice(event_types),
        "product_id": random.choice(products),
        "price": round(random.uniform(10, 200), 2),
        "event_time": datetime.utcnow().isoformat(),
        "device": random.choice(devices),
        "country": random.choice(countries)
    }

    # Send event to Kafka topic
    producer.send(TOPIC_RAW, value=event)

    print(f"Sent: {event['event_type']} by {event['user_id']}")

    time.sleep(random.uniform(0.5, 2))
