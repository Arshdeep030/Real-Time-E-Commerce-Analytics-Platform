#!/bin/bash

KAFKA_CONTAINER=kafka
BOOTSTRAP_SERVER=localhost:9092

echo "Creating Kafka topics..."

docker exec $KAFKA_CONTAINER kafka-topics \
  --bootstrap-server $BOOTSTRAP_SERVER \
  --create \
  --topic ecommerce_events_raw \
  --partitions 3 \
  --replication-factor 1

docker exec $KAFKA_CONTAINER kafka-topics \
  --bootstrap-server $BOOTSTRAP_SERVER \
  --create \
  --topic ecommerce_events_enriched \
  --partitions 3 \
  --replication-factor 1

docker exec $KAFKA_CONTAINER kafka-topics \
  --bootstrap-server $BOOTSTRAP_SERVER \
  --create \
  --topic dead_letter_queue \
  --partitions 1 \
  --replication-factor 1

echo "Kafka topics created successfully."
