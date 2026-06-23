# Environmental Monitoring System

## Project Description

This project implements an IoT Environmental Monitoring System using MQTT and Python.

The system simulates environmental sensors, transmits data through an MQTT broker, processes the data in Python, and stores it in multiple database platforms.

## Technologies Used

* Python
* Eclipse Mosquitto (MQTT Broker)
* MySQL
* MongoDB
* Neo4j
* Streamlit

## Features

* Real-time MQTT communication
* Temperature data storage in MySQL
* Humidity data storage in MongoDB
* Sensor relationship modeling in Neo4j
* Real-time dashboard using Streamlit
* Data visualization using charts and tables

## System Architecture

Publisher → MQTT Broker → Subscriber → Databases

Databases:

* MySQL (structured sensor measurements)
* MongoDB (document-oriented sensor/device data)
* Neo4j (sensor relationships)

Dashboard:

* Streamlit visualization layer

## Author

Surafel Hunegnaw
