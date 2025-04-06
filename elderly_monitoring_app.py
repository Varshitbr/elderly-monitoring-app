import pandas as pd
import requests
import streamlit as st
st.set_page_config(page_title="Elderly Monitoring", layout="centered", page_icon="🧓")
st.title("👵 Elderly Monitoring Dashboard")
# CONFIG
MODEL = "tinyllama"
OLLAMA_API = "http://localhost:11434/api/generate"

# LOAD DATA
@st.cache_data
def load_data():
    health = pd.read_csv("health_monitoring.csv")
    safety = pd.read_csv("safety_monitoring.csv")
    reminder = pd.read_csv("reminder.csv")
    return health, safety, reminder

health_df, safety_df, reminder_df = load_data()

# AGENTS
def health_monitor(df):
    alerts = []
    abnormal = df[df['Alert Triggered (Yes/No)'] == 'Yes']
    for _, row in abnormal.iterrows():
        alerts.append(f"🩺 **Health Alert** for `{row['Device-ID/User-ID']}` | HR: {row['Heart Rate']}, BP: {row['Blood Pressure']}, Glucose: {row['Glucose Levels']}")
    return alerts

def safety_monitor(df):
    alerts = []
    events = df[df['Fall Detected (Yes/No)'] == 'Yes']
    for _, row in events.iterrows():
        alerts.append(f"⚠️ **Fall Detected** for `{row['Device-ID/User-ID']}` at {row['Location']} on {row['Timestamp']}")
    return alerts

def reminder_agent(df):
    alerts = []
    pending = df[df['Reminder Sent (Yes/No)'] == 'No']
    for _, row in pending.iterrows():
        alerts.append(f"⏰ **Reminder** for `{row['Device-ID/User-ID']}`: {row['Reminder Type']} at {row['Scheduled Time']}")
    return alerts

def ollama_ai_summary(alerts):
    prompt = "You are an elderly care assistant. Summarize these alerts in a helpful, empathetic way:\n\n" + "\n".join(alerts)
    response = requests.post(OLLAMA_API, json={"model": MODEL, "prompt": prompt})
    try:
        return response.json().get("response", "⚠️ No summary from AI")
    except Exception as e:
        return f"❌ Ollama error: {e}"

# STREAMLIT UI

st.markdown("Monitor health, safety, and reminders for elderly individuals using AI-powered insights.")

if st.button("🔍 Run Analysis"):
    with st.spinner("Analyzing alerts..."):
        alerts = health_monitor(health_df) + safety_monitor(safety_df) + reminder_agent(reminder_df)

    if not alerts:
        st.success("✅ No current alerts.")
    else:
        with st.expander("📋 View Raw Alerts"):
            for alert in alerts:
                st.markdown(f"- {alert}")

        st.subheader("🧠 AI-Powered Summary")
        with st.spinner("Generating summary with TinyLLaMA..."):
            summary = ollama_ai_summary(alerts)
        st.info(summary)

st.markdown("---")
st.caption("Developed by CareTrackers 🚀 | Powered by Streamlit + Ollama AI")
