import json

import mysql.connector
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from neo4j import GraphDatabase

from config import *

# ==========================
# MySQL
# ==========================

mysql_db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

mysql_cursor = mysql_db.cursor()

# ==========================
# MongoDB
# ==========================

mongo_client = MongoClient(MONGO_URI)

mongo_db = mongo_client[MONGO_DATABASE]

device_collection = mongo_db["devices"]

# ==========================
# Neo4j
# ==========================

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


# ==========================
# MQTT
# ==========================

def on_connect(client, userdata, flags, reason_code, properties=None):

    print("Connected to MQTT Broker")

    client.subscribe(TOPIC_MEASUREMENT)
    client.subscribe(TOPIC_DEVICE)
    client.subscribe(TOPIC_NETWORK)


def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode())

    # =====================================
    # MySQL
    # =====================================

    if msg.topic == TOPIC_MEASUREMENT:

        sql = """
        INSERT INTO measurements
        (sensor_id, temperature, humidity, timestamp)
        VALUES (%s,%s,%s,%s)
        """

        values = (
            data["sensor_id"],
            data["temperature"],
            data["humidity"],
            data["timestamp"]
        )

        mysql_cursor.execute(sql, values)

        mysql_db.commit()

        print("Measurement -> MySQL")

    # =====================================
    # MongoDB
    # =====================================

    elif msg.topic == TOPIC_DEVICE:

        device_collection.update_one(

            {

                "_id": data["sensor_id"]

            },

            {

                "$set": {

                    "manufacturer": data["manufacturer"],
                    "model": data["model"],
                    "battery": data["battery"],
                    "firmware": data["firmware"],
                    "status": data["status"],
                    "last_seen": data["last_seen"]

                }

            },

            upsert=True

        )

        print("Device -> MongoDB")

    # =====================================
    # Neo4j
    # =====================================

    elif msg.topic == TOPIC_NETWORK:

        with driver.session() as session:

            session.run("""

            MERGE (s:Sensor {id:$sensor})

            MERGE (r:Room {name:$room})

            MERGE (b:Building {name:$building})

            MERGE (g:Gateway {name:$gateway})

            MERGE (s)-[:LOCATED_IN]->(r)

            MERGE (r)-[:PART_OF]->(b)

            MERGE (s)-[:CONNECTED_TO]->(g)

            """,

            sensor=data["sensor_id"],

            room=data["room"],

            building=data["building"],

            gateway=data["gateway"]

            )

        print("Network -> Neo4j")

    print(data)

    print("-" * 60)


client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT)

client.loop_forever()
