import streamlit as st
import pandas as pd

st.set_page_config(page_title="👵 Elderly Monitoring Dashboard", layout="wide")

st.title("👵 Elderly Monitoring Dashboard")

# Upload health CSV
health_file = st.file_uploader("📋 Upload Health Monitoring CSV", type="csv", key="health")
if health_file is not None:
    health_df = pd.read_csv(health_file)
else:
    health_df = pd.DataFrame(columns=["Date", "Heart Rate", "Blood Pressure"])
    st.info("Please upload a health CSV to view data.")

# Upload safety CSV
safety_file = st.file_uploader("🛡️ Upload Safety Monitoring CSV", type="csv", key="safety")
if safety_file is not None:
    safety_df = pd.read_csv(safety_file)
else:
    safety_df = pd.DataFrame(columns=["Date", "Fall Detected", "Location"])
    st.info("Please upload a safety CSV to view data.")

# Upload reminders CSV
reminder_file = st.file_uploader("⏰ Upload Medication Reminders CSV", type="csv", key="reminder")
if reminder_file is not None:
    reminder_df = pd.read_csv(reminder_file)
else:
    reminder_df = pd.DataFrame(columns=["Date", "Time", "Medication"])
    st.info("Please upload a reminders CSV to view data.")

# Display tables
with st.expander("📊 Health Data"):
    st.dataframe(health_df)

with st.expander("🛡️ Safety Data"):
    st.dataframe(safety_df)

with st.expander("⏰ Reminders"):
    st.dataframe(reminder_df)
