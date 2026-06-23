# Environmental Monitoring System

## Overview

This project implements an IoT Environmental Monitoring System using MQTT, Python, MySQL, MongoDB, Neo4j, and Streamlit.

The system simulates environmental sensors that generate temperature and humidity data. The generated data is transmitted through an MQTT broker, processed by a Python subscriber, and stored in multiple database platforms according to the nature of the data. A Streamlit dashboard provides real-time visualization of the collected information.

The project demonstrates the integration of different database technologies within a single IoT application and highlights the advantages of relational, document-oriented, and graph databases.

---

## Project Objectives

The main objectives of this project are:

* Simulate environmental IoT sensors.
* Collect sensor data using MQTT.
* Process incoming messages using Python.
* Store structured data in MySQL.
* Store document-oriented data in MongoDB.
* Model relationships using Neo4j.
* Visualize collected data through a Streamlit dashboard.
* Demonstrate the use of multiple database technologies in a single system.

---

## Technologies Used

### Programming Language

* Python

### Messaging Protocol

* MQTT

### MQTT Broker

* Eclipse Mosquitto

### Databases

* MySQL
* MongoDB
* Neo4j

### Dashboard and Visualization

* Streamlit
* Pandas
* Plotly

---

## System Architecture

Environmental Sensor Simulator

↓

MQTT Publisher

↓

Mosquitto MQTT Broker

↓

Python Subscriber

↓

MySQL (Structured Sensor Data)

MongoDB (Document-Based Sensor Data)

Neo4j (Sensor Relationships)

↓

Streamlit Dashboard

---

## Database Design

### MySQL

MySQL is used to store structured environmental measurements such as:

* Sensor ID
* Temperature
* Timestamp

Relational databases are suitable for highly structured and tabular data.

### MongoDB

MongoDB is used to store flexible sensor and environmental information in document format.

Example document:

{
"sensor": "humidity_sensor_1",
"humidity": 65.2,
"timestamp": "2026-06-23"
}

Document databases provide flexibility for storing semi-structured data.

### Neo4j

Neo4j is used to model relationships among:

* Sensors
* Gateways
* Rooms

Example:

Sensor → Gateway → Room

Graph databases are ideal for representing connected entities and relationships.

---

## Features

* Real-time MQTT communication
* Environmental sensor simulation
* Temperature data storage in MySQL
* Humidity data storage in MongoDB
* Relationship modeling in Neo4j
* Interactive Streamlit dashboard
* Data visualization using charts and tables
* Multi-database integration

---

## Project Files

publisher.py

Simulates environmental sensors and publishes MQTT messages.

subscriber.py

Receives MQTT messages and stores data in the databases.

dashboard.py

Displays real-time environmental information through a Streamlit dashboard.

requirements.txt

Contains all required Python libraries.

README.md

Project documentation.

---

## Installation

### Install Required Libraries

pip install -r requirements.txt

### Start MongoDB

Start the MongoDB service and connect using MongoDB Compass.

### Start MySQL

Open MySQL Workbench and connect to the local instance.

### Start Neo4j

Open Neo4j Desktop and start the database.

### Start MQTT Subscriber

python subscriber.py

### Start MQTT Publisher

python publisher.py

### Launch Dashboard

streamlit run dashboard.py

---

## Dashboard

The Streamlit dashboard displays:

* Current temperature values
* Current humidity values
* Number of records stored in MySQL
* Number of documents stored in MongoDB
* Temperature charts
* Humidity charts
* Database tables

The dashboard provides a user-friendly interface for monitoring environmental data in real time.

---

## Future Improvements

Possible future enhancements include:

* Integration with real IoT sensors
* Air quality monitoring
* Cloud deployment
* Apache Spark integration for big data analytics
* Machine learning prediction models
* Mobile application support
* Docker containerization

---

## Author

Surafel Hunegnaw

GitHub Username: blackredws

Repository:

https://github.com/blackredws/EnvironmentalMonitoring

---

## Conclusion

This project successfully demonstrates the integration of MQTT, Python, MySQL, MongoDB, Neo4j, and Streamlit in a unified environmental monitoring platform.

The system collects sensor data, processes it in real time, stores it using multiple database technologies, and visualizes the results through an interactive dashboard. The project provides a practical example of modern IoT and database integration techniques.
