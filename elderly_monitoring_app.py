
import streamlit as st
st.set_page_config(page_title="Elderly Monitoring", layout="centered", page_icon="🧓")
import pandas as pd
import requests
st.title("👵 Elderly Monitoring Dashboard")

MODEL = "tinyllama"
OLLAMA_API = "http://localhost:11434/api/generate"

# LOAD DATA
@st.cache_data
def load_data():
    health = pd.read_csv("C:/Users/Varshit b r/Downloads/health_monitoring.csv")
    safety = pd.read_csv("C:/Users/Varshit b r/Downloads/safety_monitoring.csv")
    reminder = pd.read_csv("C:/Users/Varshit b r/Downloads/daily_reminder.csv")
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
    import json

    prompt = "You are an elderly care assistant. Summarize these alerts in a friendly, helpful way:\n\n" + "\n".join(alerts)

    try:
        response = requests.post(OLLAMA_API, json={"model": MODEL, "prompt": prompt}, stream=True)
        summary = ""

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    summary += data.get("response", "")
                except json.JSONDecodeError:
                    pass  # skip malformed chunks

        return summary if summary else "⚠️ No summary generated."
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
