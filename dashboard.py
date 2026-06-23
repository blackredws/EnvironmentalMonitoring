import streamlit as st
import pandas as pd
import mysql.connector
from pymongo import MongoClient

st.set_page_config(
    page_title="Environmental Monitoring Dashboard",
    layout="wide"
)

st.title("🌍 Environmental Monitoring Dashboard")

# ==========================
# MySQL Connection
# ==========================

mysql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sura@1221",
    database="environmental_monitoring"
)

query = """
SELECT *
FROM temperature_data
ORDER BY timestamp DESC
"""

temperature_df = pd.read_sql(query, mysql_db)

# ==========================
# MongoDB Connection
# ==========================

mongo_client = MongoClient("mongodb://localhost:27017")

mongo_db = mongo_client["environmental_monitoring"]

humidity_collection = mongo_db["humidity_data"]

humidity_docs = list(
    humidity_collection.find(
        {},
        {"_id": 0}
    )
)

humidity_df = pd.DataFrame(humidity_docs)

# ==========================
# Metrics
# ==========================

col1, col2, col3, col4 = st.columns(4)

if not temperature_df.empty:
    latest_temp = temperature_df.iloc[0]["temperature"]
else:
    latest_temp = 0

if not humidity_df.empty:
    latest_humidity = humidity_df.iloc[-1]["humidity"]
else:
    latest_humidity = 0

col1.metric(
    "Current Temperature",
    f"{latest_temp} °C"
)

col2.metric(
    "Current Humidity",
    f"{latest_humidity} %"
)

col3.metric(
    "MySQL Records",
    len(temperature_df)
)

col4.metric(
    "MongoDB Documents",
    len(humidity_df)
)

st.divider()

# ==========================
# Temperature Chart
# ==========================

st.subheader("🌡 Temperature Data")

if not temperature_df.empty:

    chart_df = temperature_df.sort_values(
        by="timestamp"
    )

    st.line_chart(
        chart_df.set_index("timestamp")["temperature"]
    )

    st.dataframe(
        temperature_df.head(20)
    )

# ==========================
# Humidity Chart
# ==========================

st.subheader("💧 Humidity Data")

if not humidity_df.empty:

    humidity_df["timestamp"] = pd.to_datetime(
        humidity_df["timestamp"]
    )

    humidity_df = humidity_df.sort_values(
        by="timestamp"
    )

    st.line_chart(
        humidity_df.set_index("timestamp")["humidity"]
    )

    st.dataframe(
        humidity_df.tail(20)
    )