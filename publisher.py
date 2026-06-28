import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

from config import (
    MQTT_BROKER,
    MQTT_PORT,
    TOPIC_MEASUREMENT,
    TOPIC_DEVICE,
    TOPIC_NETWORK,
)

from sensors import SENSORS

client = mqtt.Client()

client.connect(MQTT_BROKER, MQTT_PORT)

print("=" * 60)
print("SMART CAMPUS ENVIRONMENTAL MONITORING SYSTEM")
print("=" * 60)

while True:

    print("\nPublishing Sensor Data...\n")

    for sensor in SENSORS:

        room = sensor["room"]

        # -------------------------
        # Generate realistic values
        # -------------------------

        if room == "Greenhouse":

            temperature = round(random.uniform(28, 35), 2)
            humidity = round(random.uniform(70, 90), 2)

        elif "Lab" in room:

            temperature = round(random.uniform(20, 25), 2)
            humidity = round(random.uniform(40, 60), 2)

        elif room == "Storage":

            temperature = round(random.uniform(15, 22), 2)
            humidity = round(random.uniform(35, 50), 2)

        else:

            temperature = round(random.uniform(21, 27), 2)
            humidity = round(random.uniform(45, 65), 2)

        # -------------------------
        # Measurement
        # -------------------------

        measurement = {

            "sensor_id": sensor["sensor_id"],
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": str(datetime.now())

        }

        client.publish(
            TOPIC_MEASUREMENT,
            json.dumps(measurement)
        )

        # -------------------------
        # Device
        # -------------------------

        device = {

            "sensor_id": sensor["sensor_id"],
            "manufacturer": sensor["manufacturer"],
            "model": random.choice(["BME280", "DHT22", "SHT31"]),
            "battery": random.randint(70, 100),
            "firmware": random.choice(["1.0.0", "2.0.1", "2.1.3"]),
            "status": random.choice(["ACTIVE", "ACTIVE", "ACTIVE", "MAINTENANCE"]),
            "last_seen": str(datetime.now())

        }

        client.publish(
            TOPIC_DEVICE,
            json.dumps(device)
        )

        # -------------------------
        # Network
        # -------------------------

        network = {

            "sensor_id": sensor["sensor_id"],
            "building": sensor["building"],
            "room": sensor["room"],
            "gateway": sensor["gateway"]

        }

        client.publish(
            TOPIC_NETWORK,
            json.dumps(network)
        )

        print(
            f'{sensor["sensor_id"]} | '
            f'{temperature}°C | '
            f'{humidity}% | '
            f'{device["battery"]}% Battery'
        )

    print("-" * 60)

    time.sleep(5)
