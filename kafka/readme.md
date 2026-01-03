# Kafka Setup for Real-Time E-Commerce Analytics

This module sets up a **local Kafka environment** to simulate a real-time streaming platform for e-commerce events.  
It uses **Docker Desktop** (Apple Silicon compatible) and creates the Kafka topics that will be used in the pipeline.

---

## 🚀 Purpose

- Provide a **messaging backbone** for the project
- Simulate **real-time event ingestion** from the frontend
- Enable **Spark Structured Streaming** to consume events
- Include a **dead-letter queue** for handling bad or corrupted events
- Establish **production-style topic design** with partitions


## What it does:

- Acts as a messaging system — a middleman between data generator and Spark streaming.
- Stores events temporarily until Spark or any consumer reads them.
- Supports multiple topics:
    - ecommerce_events_raw → raw events straight from generator
    - ecommerce_events_enriched → processed events later
    - dead_letter_queue → bad/corrupt events

## How Kafka works in your setup:

- Zookeeper → manages Kafka metadata and brokers. Think of it as the traffic controller.
- Kafka broker → the actual messaging server. Stores events in topics.
- Topics → like “buckets” where events are sent.
- Partitions → each topic is split into multiple partitions for parallelism.
- Docker → makes it easy to run Kafka + Zookeeper locally, without installing anything manually.

## How Data Generator + Kafka Connect

Right now, your data generator prints events to the console.
Later (next step):

- Instead of printing, it will send events to Kafka using a Kafka Python client.
- Kafka will receive the event and store it in the chosen topic (ecommerce_events_raw).
- Spark streaming or any consumer can read events from Kafka in real-time, process them, and store results in S3.

### Think of it as a conveyor belt:
- Data Generator → Kafka topic (ecommerce_events_raw) → Spark Streaming → S3/Athena/dbt

- Generator = “factory producing products (events)”
- Kafka = “conveyor belt storing and moving products”
- Spark = “worker that inspects and processes products”







