import json
from datetime import datetime

import mysql.connector
import paho.mqtt.client as mqtt
from pymongo import MongoClient

BROKER = "localhost"
PORT = 1883

# ==========================
# MySQL Connection
# ==========================

mysql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sura@1221",
    database="environmental_monitoring"
)

mysql_cursor = mysql_db.cursor()

# ==========================
# MongoDB Connection
# ==========================

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["environmental_monitoring"]
humidity_collection = mongo_db["humidity_data"]


# ==========================
# MQTT Functions
# ==========================

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected to MQTT Broker")

    client.subscribe("environment/temperature")
    client.subscribe("environment/humidity")


def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode())

    # --------------------------
    # Temperature -> MySQL
    # --------------------------
    if msg.topic == "environment/temperature":

        sensor = data["sensor"]
        temperature = data["temperature"]
        timestamp = datetime.now()

        sql = """
        INSERT INTO temperature_data
        (sensor, temperature, timestamp)
        VALUES (%s, %s, %s)
        """

        values = (sensor, temperature, timestamp)

        mysql_cursor.execute(sql, values)
        mysql_db.commit()

        print("\nStored Temperature in MySQL")
        print(data)

    # --------------------------
    # Humidity -> MongoDB
    # --------------------------
    elif msg.topic == "environment/humidity":

        document = {
            "sensor": data["sensor"],
            "humidity": data["humidity"],
            "timestamp": datetime.now()
        }

        humidity_collection.insert_one(document)

        print("\nStored Humidity in MongoDB")
        print(document)

    print("-" * 50)


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

client.loop_forever()