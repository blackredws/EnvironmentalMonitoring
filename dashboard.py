import streamlit as st
import pandas as pd
import mysql.connector
from pymongo import MongoClient
from neo4j import GraphDatabase
from config import *

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Smart Campus Environmental Monitoring",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Smart Campus Environmental Monitoring System")
st.markdown("---")

# =====================================
# MYSQL CONNECTION
# =====================================

mysql_db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

# =====================================
# MONGODB CONNECTION
# =====================================

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DATABASE]
device_collection = mongo_db["devices"]

# =====================================
# NEO4J CONNECTION
# =====================================

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)

# =====================================
# LOAD MYSQL DATA
# =====================================

measurement_query = """
SELECT *
FROM measurements
ORDER BY timestamp DESC
LIMIT 300
"""

measurement_df = pd.read_sql(measurement_query, mysql_db)

alert_query = """
SELECT *
FROM alerts
ORDER BY timestamp DESC
LIMIT 100
"""
alerts_df = pd.read_sql(alert_query, mysql_db)

# =====================================
# LOAD MONGODB DATA
# =====================================

devices = list(
    device_collection.find(
        {},
        {"_id": 0}
    )
)

device_df = pd.DataFrame(devices)

# =====================================
# LOAD NEO4J SUMMARY
# =====================================

with driver.session() as session:

    sensor_count = session.run(
        "MATCH (s:Sensor) RETURN count(s) AS c"
    ).single()["c"]

    room_count = session.run(
        "MATCH (r:Room) RETURN count(r) AS c"
    ).single()["c"]

    building_count = session.run(
        "MATCH (b:Building) RETURN count(b) AS c"
    ).single()["c"]

    gateway_count = session.run(
        "MATCH (g:Gateway) RETURN count(g) AS c"
    ).single()["c"]

# =====================================
# LATEST VALUES
# =====================================

if measurement_df.empty:

    latest_temp = 0
    latest_humidity = 0

else:

    latest_temp = measurement_df.iloc[0]["temperature"]
    latest_humidity = measurement_df.iloc[0]["humidity"]

# =====================================
# SMART STATUS
# =====================================

status = "🟢 NORMAL"
recommendation = "Environment operating within safe limits."

if latest_temp > 35:

    status = "🔴 HIGH TEMPERATURE"

    recommendation = (
        "Activate cooling system immediately."
    )

elif latest_humidity > 80:

    status = "🟡 HIGH HUMIDITY"

    recommendation = (
        "Increase room ventilation."
    )

# =====================================
# STATUS PANEL
# =====================================

st.subheader("🚦 System Status")

if "🔴" in status:

    st.error(status)

elif "🟡" in status:

    st.warning(status)

else:

    st.success(status)

st.info(recommendation)

st.markdown("---")

# =====================================
# METRICS
# =====================================

avg_temp = (
    measurement_df["temperature"].mean()
    if not measurement_df.empty
    else 0
)

avg_humidity = (
    measurement_df["humidity"].mean()
    if not measurement_df.empty
    else 0
)

max_temp = (
    measurement_df["temperature"].max()
    if not measurement_df.empty
    else 0
)

max_humidity = (
    measurement_df["humidity"].max()
    if not measurement_df.empty
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Temperature",
    f"{latest_temp:.2f} °C"
)

col2.metric(
    "Current Humidity",
    f"{latest_humidity:.2f} %"
)

col3.metric(
    "Measurements",
    len(measurement_df)
)

col4.metric(
    "Alerts",
    len(alerts_df)
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Average Temp",
    f"{avg_temp:.2f} °C"
)

col6.metric(
    "Average Humidity",
    f"{avg_humidity:.2f} %"
)

col7.metric(
    "Maximum Temp",
    f"{max_temp:.2f} °C"
)

col8.metric(
    "Maximum Humidity",
    f"{max_humidity:.2f} %"
)

st.markdown("---")
# =====================================
# TEMPERATURE CHART
# =====================================

st.subheader("🌡 Temperature Trend")

if not measurement_df.empty:

    temp_chart = measurement_df.copy()

    temp_chart["timestamp"] = pd.to_datetime(
        temp_chart["timestamp"]
    )

    temp_chart = temp_chart.sort_values("timestamp")

    st.line_chart(
        temp_chart.set_index("timestamp")["temperature"]
    )

else:

    st.warning("No temperature data available.")

# =====================================
# HUMIDITY CHART
# =====================================

st.subheader("💧 Humidity Trend")

if not measurement_df.empty:

    humidity_chart = measurement_df.copy()

    humidity_chart["timestamp"] = pd.to_datetime(
        humidity_chart["timestamp"]
    )

    humidity_chart = humidity_chart.sort_values("timestamp")

    st.line_chart(
        humidity_chart.set_index("timestamp")["humidity"]
    )

else:

    st.warning("No humidity data available.")

st.markdown("---")

# =====================================
# LATEST MEASUREMENTS
# =====================================

st.subheader("📊 Latest Measurements")

if measurement_df.empty:

    st.info("No measurements found.")

else:

    st.dataframe(
        measurement_df.head(15),
        use_container_width=True
    )

st.markdown("---")

# =====================================
# ALERTS
# =====================================

st.subheader("🚨 Latest Alerts")

if alerts_df.empty:

    st.success("No alerts have been generated.")

else:

    latest_alert = alerts_df.iloc[0]

    if latest_alert["severity"] == "Critical":

        st.error(
            f"{latest_alert['alert_type']} - {latest_alert['message']}"
        )

    elif latest_alert["severity"] == "Warning":

        st.warning(
            f"{latest_alert['alert_type']} - {latest_alert['message']}"
        )

    st.dataframe(
        alerts_df.head(10),
        use_container_width=True
    )

st.markdown("---")

# =====================================
# DEVICES (MongoDB)
# =====================================

st.subheader("📱 Registered Devices (MongoDB)")

if device_df.empty:

    st.info("No devices found.")

else:

    st.metric(
        "Registered Devices",
        len(device_df)
    )

    st.dataframe(
        device_df,
        use_container_width=True
    )

st.markdown("---")

# =====================================
# NEO4J SUMMARY
# =====================================

st.subheader("🌐 Campus Network (Neo4j)")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Sensors",
    sensor_count
)

c2.metric(
    "Rooms",
    room_count
)

c3.metric(
    "Buildings",
    building_count
)

c4.metric(
    "Gateways",
    gateway_count
)

st.markdown("---")

# =====================================
# PROJECT INFORMATION
# =====================================

with st.expander("ℹ Project Information"):

    st.write("""
This project demonstrates an IoT Environmental Monitoring System.

Technologies Used

• Python

• MQTT (Mosquitto)

• MySQL

• MongoDB

• Neo4j

• Streamlit

Database Usage

• MySQL stores environmental measurements.

• MongoDB stores device metadata.

• Neo4j stores the relationships between sensors,
  rooms, gateways and buildings.

Developed for Database Mod B.
""")

st.markdown("---")

st.caption(
    "Smart Campus Environmental Monitoring System | University of Messina"
)

