from confluent_kafka import Consumer, Producer
import json
import sqlite3
import os
from dotenv import load_dotenv

# Učitaj .env fajl
load_dotenv()

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
TOPIC = os.environ.get("KAFKA_TOPIC", "sensor_readings")
GROUP_ID = os.environ.get("KAFKA_GROUP_ID", "sensors_consumers")
DLQ_TOPIC = "sensor_readings_glq"

dlq_producer = Producer({"bootstrap.servers": KAFKA_BROKER})

def validate_event(event):
    if "temperature" in event.get("payload", {}):
        if event["payload"]["temperature"] < -50 or event["payload"]["temperature"] >100:
            return False
    required_fields=["event_id", "event_type", "timestamp", "business_id", "payload"]
    for field in required_fields:
        if field not in event:
            return False
    return True

def save_event(event):
    conn=sqlite3.connect("sensors.db")
    cursor=conn.cursor()
    try:
        cursor.execute('''
                    INSERT INTO events (event_id, event_type, business_id, timestamp, payload)
                    VALUES (?, ?, ?, ?, ?)
                ''', (event["event_id"], event["event_type"], event["business_id"], event["timestamp"],
                      json.dumps(event["payload"])))
        conn.commit()
    except:
        print(f"Event {event['event_id']} already exists. Skipping.")
        conn.close()

consumer_conf = {
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": GROUP_ID,
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC])


while True:
    msg=consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
    event = json.loads(msg.value().decode("utf-8"))
    if validate_event(event):
        print(f"Processed event {event['event_id']} from partition {msg.partition()}")
        save_event(event)
    else:
        print(f"Invalid event {event['event_id']}, send to DLQ")
        dlq_producer.produce(DLQ_TOPIC, key=event.get("business_id"), value=json.dumps(event))
        dlq_producer.flush()

consumer.close()
