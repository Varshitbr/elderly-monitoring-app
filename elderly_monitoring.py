import pandas as pd
import requests

# Config
MODEL = "tinyllama"  # or gemma / phi / mistral
OLLAMA_API = "http://localhost:11434/api/generate"

# Load datasets
health_df = pd.read_csv("C:/Users/Varshit b r/Downloads/health_monitoring.csv")
safety_df = pd.read_csv("C:/Users/Varshit b r/Downloads/safety_monitoring.csv")
reminder_df = pd.read_csv("C:/Users/Varshit b r/Downloads/daily_reminder.csv")

# Agent 1: Health Monitor
def health_monitor(df):
    alerts = []
    abnormal = df[df['Alert Triggered (Yes/No)'] == 'Yes']
    for _, row in abnormal.iterrows():
        alerts.append(f"Health Alert for {row['Device-ID/User-ID']}: HR={row['Heart Rate']}, BP={row['Blood Pressure']}, Glucose={row['Glucose Levels']}")
    return alerts

# Agent 2: Safety Monitor
def safety_monitor(df):
    alerts = []
    events = df[df['Fall Detected (Yes/No)'] == 'Yes']
    for _, row in events.iterrows():
        alerts.append(f"Safety Alert: Fall detected for {row['Device-ID/User-ID']} at {row['Location']} on {row['Timestamp']}")
    return alerts

# Agent 3: Reminder Agent
def reminder_agent(df):
    alerts = []
    pending = df[df['Reminder Sent (Yes/No)'] == 'No']
    for _, row in pending.iterrows():
        alerts.append(f"Reminder for {row['Device-ID/User-ID']}: {row['Reminder Type']} at {row['Scheduled Time']}")
    return alerts

# AI Summary via Ollama
def ollama_ai_summary(alerts):
    prompt = "You are an elderly care assistant. Summarize these alerts in a friendly, helpful way:\n\n" + "\n".join(alerts)
    response = requests.post(OLLAMA_API, json={"model": MODEL, "prompt": prompt})
    try:
        return response.json().get("response", "⚠️ No summary from AI")
    except Exception as e:
        return f"❌ Ollama error: {e}"

# Main system runner
def run():
    alerts = health_monitor(health_df) + safety_monitor(safety_df) + reminder_agent(reminder_df)

    if not alerts:
        print("✅ No current alerts.")
        return

    print("📋 Raw Alerts:")
    for a in alerts:
        print("•", a)

    print("\n🧠 Ollama AI Summary:")
    summary = ollama_ai_summary(alerts)
    print(summary)

# Execute
run()
