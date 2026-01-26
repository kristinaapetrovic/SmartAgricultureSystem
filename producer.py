import json
import uuid
import random
import time
from datetime import datetime
from confluent_kafka import Producer

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

TOPIC="sensor_readings"

sensor_ids=["sensor_001", "sensor_002", "sensor_003"]

def generate_event():
    event_types=["temperature_reading", "humidity_reading", "soil_moisture_reading", "plant_health_alert"]
    alerts=["pest_detected", "disease_detected", "wilting"]
    event_type=random.choice(event_types)
    sensor_id=random.choice(sensor_ids)
    alert=random.choice(alerts)

    payload={}

    if event_type == "temperature_reading":
        payload["temperature"] = round(random.uniform(-15, 35), 1)
        if random.random() < 0.1:
            payload["temperature"] = -100
    elif event_type == "humidity_reading":
        payload["humidity"] = round(random.uniform(-30, 90), 1)
    elif event_type == "soil_moisture_reading":
        payload["soil_moisture"] = round(random.uniform(0, 100), 1)
    elif event_type == "plant_health_alert":
        payload["alert"] = alert

    event={
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat()+ "Z",
        "business_id": sensor_id,
        "payload": payload
    }

    return event, sensor_id

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed for message {msg.key()}: {err}")
    else:
        print(f"Messgae delivered to {msg.topic()} partition {msg.partition()}")

if __name__ == '__main__':
    while True:
        event, key = generate_event()
        producer.produce(TOPIC, key=key, value=json.dumps(event), on_delivery=delivery_report)
        producer.flush()
        time.sleep(2)



