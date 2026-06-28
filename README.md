# 🌍 Smart Campus Environmental Monitoring System

## Database Mod B Project

**University of Messina**
**Academic Year:** 2025/2026

**Student:** Surafel Hunegnaw

---

# Project Overview

This project demonstrates a complete Internet of Things (IoT) environmental monitoring system using **MQTT**, **Python**, **MySQL**, **MongoDB**, **Neo4j**, and **Streamlit**.

The system simulates environmental sensors installed across a smart campus. These sensors periodically generate temperature, humidity, device, and network information.

Python applications receive MQTT messages and automatically store each type of information in the most appropriate database.

Finally, a Streamlit dashboard visualizes the collected data in real time.

---

# Technologies

* Python
* Eclipse Mosquitto MQTT Broker
* MySQL
* MongoDB
* Neo4j
* Streamlit
* Pandas
* Paho MQTT

---

# System Architecture

```
Publisher.py
        │
        ▼
 MQTT Broker (Mosquitto)
        │
        ▼
 Subscriber.py
        │
 ┌──────┼─────────┐
 ▼      ▼         ▼
MySQL MongoDB   Neo4j
        │
        ▼
 Streamlit Dashboard
```

---

# Database Responsibilities

## MySQL

Stores structured environmental measurements.

Table:

* measurements

Contains:

* Sensor ID
* Temperature
* Humidity
* Timestamp

Another table:

* alerts

Automatically populated using a MySQL AFTER INSERT Trigger whenever dangerous environmental conditions are detected.

---

## MongoDB

Stores flexible device metadata.

Each document contains:

* Sensor ID
* Manufacturer
* Model
* Firmware
* Battery
* Device Status
* Last Seen

---

## Neo4j

Models relationships between:

* Sensors
* Rooms
* Buildings
* Gateways

This allows efficient graph traversal and visualization of the smart campus network.

---

# MQTT Topics

| Topic                   | Database |
| ----------------------- | -------- |
| environment/measurement | MySQL    |
| environment/device      | MongoDB  |
| environment/network     | Neo4j    |

---

# Dashboard Features

* Live Temperature
* Live Humidity
* System Status
* Automatic Alert Display
* Temperature Chart
* Humidity Chart
* Measurements Table
* Alerts Table
* Device Information
* Campus Network Summary

---

# Business Rules

1. Each sensor has a unique Sensor ID.

2. Every environmental measurement belongs to one sensor.

3. Measurements are stored in MySQL.

4. Device metadata is stored in MongoDB.

5. Network topology is stored in Neo4j.

6. Dangerous environmental conditions automatically generate alerts through a MySQL Trigger.

---

# Project Workflow

1. Publisher simulates IoT sensors.

2. MQTT Broker forwards messages.

3. Subscriber receives MQTT topics.

4. Subscriber stores each message in the correct database.

5. Streamlit reads data from all databases.

6. Dashboard visualizes the environmental monitoring system.

---

# Installation

Install dependencies

```
pip install -r requirements.txt
```

Run the MQTT Broker.

Run:

```
python subscriber.py
```

Open another terminal:

```
python publisher.py
```

Finally:

```
streamlit run dashboard.py
```

---

# Future Improvements

* Physical IoT sensor integration
* Cloud deployment
* Email notifications
* Predictive analytics
* Docker containerization

---

# Author

Surafel Hunegnaw

University of Messina

Database Mod B Project
