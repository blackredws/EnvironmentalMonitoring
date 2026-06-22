# Environmental Monitoring System

## Project Description

This project implements an IoT Environmental Monitoring System using MQTT and Python.

The system simulates environmental sensors that generate temperature and humidity data.

The data is transmitted through an MQTT broker (Mosquitto), processed by a Python subscriber, and stored in different database platforms:

* MySQL for temperature data
* MongoDB for humidity data
* Neo4j for sensor relationships

## Technologies Used

* Python
* Eclipse Mosquitto (MQTT Broker)
* MySQL
* MongoDB
* Neo4j

## System Architecture

Sensor Simulator → MQTT Broker → Python Subscriber → Databases

## Features

* Real-time MQTT communication
* Temperature storage in MySQL
* Humidity storage in MongoDB
* Sensor relationship management in Neo4j

## Author

Surafel Hunegnaw
