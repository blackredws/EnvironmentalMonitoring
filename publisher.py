import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

client = mqtt.Client()

client.connect(BROKER, PORT)

print("Publisher started...")

while True:
    temperature_data = {
        "sensor": "temp1",
        "temperature": round(random.uniform(20, 35), 2)
    }

    humidity_data = {
        "sensor": "hum1",
        "humidity": round(random.uniform(40, 80), 2)
    }

    client.publish(
        "environment/temperature",
        json.dumps(temperature_data)
    )

    client.publish(
        "environment/humidity",
        json.dumps(humidity_data)
    )

    print("Temperature Sent:", temperature_data)
    print("Humidity Sent:", humidity_data)

    time.sleep(5)