## Frontend Event Generator

This module simulates real-time e-commerce frontend events such as
page views, add-to-cart actions, and purchases.

### Features
- Realistic event schema
- Randomized users, products, devices
- Late-arriving events (up to 7 minutes)
- Production-style JSON events



## How it works:

- Loop forever → keeps producing events continuously (like live traffic).
- Each event is a Python dictionary.
- Converts the dictionary to JSON (json.dumps) → easy to send and read later.
- Prints the event to console (for now, before Kafka).

💡 Think of it as a fake user clicking your website, and each click gets recorded as a small JSON object.