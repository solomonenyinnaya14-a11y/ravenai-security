import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import json
import time  # ADDED FOR GIST SAVE DELAY

st.set_page_config(page_title="RavenAI V3.2", layout="wide")

# GIST MEMORY FUNCTIONS
@st.cache_data(ttl=5)
def load_attacks():
    gist_id = st.secrets["GIST_ID"]
    token = st.secrets["GITHUB_TOKEN"]
    url = f"https://api.github.com/gists/{gist_id}"
    headers = {"Authorization": f"token {token}"}
    try:
        r = requests.get(url, headers=headers)
        files = r.json()["files"]
        if "attacks.json" in files:
            content = files["attacks.json"]["content"]
            return json.loads(content)
    except:
        pass
    return []

def save_attack(ip, ua, path, method):
    gist_id = st.secrets["GIST_ID"]
    token = st.secrets["GITHUB_TOKEN"]
    attacks = load_attacks()
    attacks.append({"ip": ip, "ua": ua, "path": path, "method": method, "time": str(datetime.now())})
    data = {"files": {"attacks.json": {"content": json.dumps(attacks, indent=2)}}}
    requests.patch(f"https://api.github.com/gists/{gist_id}", headers={"Authorization": f"token {token}"}, json=data)
    time.sleep(1)  # FIX: Wait 1 sec so Gist saves before next attack

st.title("🛡️ RavenAI V3.2 - Live Threat Intelligence Dashboard")

api_key = st.sidebar.text_input("Groq API Key", type="password")

col1, col2, col3 = st.columns(3)
col1.metric("Attacks Trapped", len(load_attacks()))
col2.metric("Status", "ACTIVE" if api_key else "STANDBY")
col3.metric("Fake Data Sent", 0)

if st.button("ACTIVATE HONEYPOT", type="primary"):
    if not api_key:
        st.error("Paste Groq API Key in sidebar first")
    else:
        st.success("HONEYPOT ACTIVE")
        
        # SIMULATE 3 ATTACKS - NOW WITH 1 SEC DELAY BETWEEN EACH
        for i in range(3):
            save_attack(f"192.168.1.{100+i}", "Hacker-Bot", f"/trap/{i}", "GET")
            st.warning(f"🚨 ATTACK {i+2} TRAPPED")
        
        st.rerun()

attacks = load_attacks()
if attacks:
    df = pd.DataFrame(attacks)
    st.dataframe(df, use_container_width=True)
    st.download_button("Download Evidence", df.to_csv(index=False), "attacks.csv")
else:
    st.info("No attacks yet. Click ACTIVATE HONEYPOT to test.")
