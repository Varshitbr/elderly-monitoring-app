import streamlit as st
import pandas as pd
import altair as alt
from io import StringIO
from datetime import datetime

st.set_page_config(page_title="👵 Elderly Monitoring Dashboard", layout="wide")
st.title("👵 Elderly Monitoring Dashboard")

# Sample data
sample_health_csv = "Date,Heart Rate,Blood Pressure\n2025-04-01,72,120/80\n2025-04-02,75,122/82"
sample_safety_csv = "Date,Fall Detected,Location\n2025-04-01,No,Bedroom\n2025-04-02,Yes,Bathroom"
sample_reminder_csv = "Date,Time,Medication\n2025-04-01,08:00,Aspirin\n2025-04-02,18:00,Vitamin D"

def sample_download_button(label, data, filename):
    st.download_button(label=label, data=data, file_name=filename, mime="text/csv")

tab1, tab2, tab3 = st.tabs(["📋 Health", "🛡️ Safety", "⏰ Reminders"])

# Health Tab
with tab1:
    st.header("📋 Health Monitoring")
    health_file = st.file_uploader("Upload Health CSV", type="csv", key="health")
    sample_download_button("📥 Download Sample Health CSV", sample_health_csv, "sample_health.csv")

    if health_file:
        health_df = pd.read_csv(health_file)
        health_df.columns = health_df.columns.str.strip()
        st.success("✅ Health data uploaded!")
    else:
        health_df = pd.DataFrame(columns=["Timestamp", "Heart Rate", "Blood Pressure"])
        st.info("Upload a file to see health data.")

    st.dataframe(health_df, use_container_width=True)

    # Heart Rate Trend Chart
    if not health_df.empty:
        try:
            health_df.columns = health_df.columns.str.strip()  # 🔧 Fix whitespace
            health_df['Timestamp'] = pd.to_datetime(health_df['Timestamp'], errors='coerce')
            health_df.dropna(subset=['Timestamp'], inplace=True)
            st.subheader("📈 Heart Rate Over Time")
            chart = alt.Chart(health_df).mark_line(point=True).encode(
                x='Timestamp:T',
                y='Heart Rate:Q',
                tooltip=['Timestamp', 'Heart Rate']
            ).properties(height=400)
            st.altair_chart(chart, use_container_width=True)
        except Exception as e:
            st.error("Error generating chart: " + str(e))

# Safety Tab
with tab2:
    st.header("🛡️ Safety Monitoring")
    safety_file = st.file_uploader("Upload Safety CSV", type="csv", key="safety")
    sample_download_button("📥 Download Sample Safety CSV", sample_safety_csv, "sample_safety.csv")

    if safety_file:
        safety_df = pd.read_csv(safety_file)
        st.write("👀 Safety CSV columns:", safety_df.columns.tolist())
        st.success("✅ Safety data uploaded!")
    else:
        safety_df = pd.DataFrame(columns=["Timestamp", "Fall Detected (Yes/No)", "Location"])
        st.info("Upload a file to see safety data.")

    st.dataframe(safety_df, use_container_width=True)

    # Fall Detection Bar Chart
    if not safety_df.empty:
        try:
            # Normalize column names
            safety_df.columns = safety_df.columns.str.strip().str.lower()

            # Count only rows where a fall was detected
            fall_counts = safety_df[safety_df["Fall Detected (Yes/No)"] == "Yes"]
            fall_counts = fall_counts["location"].value_counts().reset_index()
            fall_counts.columns = ["location", "count"]

            st.subheader("📊 Fall Count by Location")
            chart = alt.Chart(fall_counts).mark_bar().encode(
                x="location",
                y="count",
                tooltip=["location", "count"]
            ).properties(height=400)

            st.altair_chart(chart, use_container_width=True)
        except Exception as e:
            st.error("Error generating fall chart: " + str(e))


# Reminders Tab
with tab3:
    st.header("⏰ Medication Reminders")
    reminder_file = st.file_uploader("Upload Reminder CSV", type="csv", key="reminder")
    sample_download_button("📥 Download Sample Reminder CSV", sample_reminder_csv, "sample_reminder.csv")

    if reminder_file:
        reminder_df = pd.read_csv(reminder_file)
        st.success("✅ Reminders uploaded!")
    else:
        reminder_df = pd.DataFrame(columns=["Date", "Time", "Medication"])
        st.info("Upload a file to see medication reminders.")

    # Editable Table
    st.subheader("📝 Edit Medication Schedule")
    reminder_df = st.data_editor(reminder_df, num_rows="dynamic", use_container_width=True)

    # Alerts for upcoming / missed meds
    now = datetime.now()
    if not reminder_df.empty:
        try:
            reminder_df["Datetime"] = pd.to_datetime(reminder_df["Date"] + " " + reminder_df["Time"])
            upcoming = reminder_df[reminder_df["Datetime"] >= now].sort_values("Datetime").head(3)
            missed = reminder_df[reminder_df["Datetime"] < now].sort_values("Datetime", ascending=False).head(3)

            st.subheader("🔔 Upcoming Medications")
            if not upcoming.empty:
                st.table(upcoming[["Date", "Time", "Medication"]])
            else:
                st.info("No upcoming medications.")

            st.subheader("⚠️ Missed Medications")
            if not missed.empty:
                st.error("Some medications may have been missed:")
                st.table(missed[["Date", "Time", "Medication"]])
            else:
                st.success("No missed medications!")
        except Exception as e:
            st.warning("Could not process medication dates: " + str(e))

    # Export edited reminders
    st.subheader("📤 Download Updated Reminders")
    csv = reminder_df.drop(columns=["Datetime"], errors="ignore").to_csv(index=False)
    st.download_button("💾 Download as CSV", data=csv, file_name="updated_reminders.csv", mime="text/csv")

