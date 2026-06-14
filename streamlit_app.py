import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(page_title="RavenAI V3.2 - Live Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ RavenAI V3.2 - Live Dashboard")
st.caption("Honeypot Security System")

# DEBUG TELEGRAM FUNCTION - SHOWS ERRORS ON PAGE
def send_telegram(message):
    token = st.secrets.get("TELEGRAM_TOKEN", "")
    chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "")
    
    # SHOW VALUES ON PAGE - REMOVE AFTER FIX
    st.write(f"**DEBUG: Token** = `{token[:20]}...`")
    st.write(f"**DEBUG: ChatID** = `{chat_id}`")
    
    if not token or not chat_id:
        st.error("❌ DEBUG: Token or ChatID is EMPTY - Check Secrets")
        return False
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=10)
        st.write(f"**DEBUG: Status** = `{r.status_code}`")
        st.write(f"**DEBUG: Response** = `{r.text}`")
        
        if r.status_code == 200:
            st.success("✅ Telegram sent!")
            return True
        else:
            st.error(f"❌ Telegram failed: {r.text}")
            return False
    except Exception as e:
        st.error(f"❌ Exception: {e}")
        return False

# HONEYPOT LOGIC
if 'trapped' not in st.session_state:
    st.session_state.trapped = []

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Attacks Trapped: {len(st.session_state.trapped)}")
    st.metric("Status", "STANDBY")
    
    if st.button("🚨 ACTIVATE HONEYPOT", type="primary"):
        fake_ip = f"192.168.{len(st.session_state.trapped)+1}.100"
        fake_ua = "Hacker-Bot/3.0"
        fake_path = f"/trap/{len(st.session_state.trapped)+2}"
        
        attack = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "ip": fake_ip,
            "ua": fake_ua,
            "path": fake_path
        }
        st.session_state.trapped.append(attack)
        
        # SEND TELEGRAM ALERT + SHOW DEBUG
        msg = f"🚨 RAVENAI ALERT\nIP: {fake_ip}\nPath: {fake_path}\nTime: {attack['time']}"
        send_telegram(msg)
        
        st.rerun()

with col2:
    st.subheader("Recent Traps")
    if st.session_state.trapped:
        for t in st.session_state.trapped[-5:]:
            st.code(f"{t['time']} | {t['ip']} | {t['path']}")
    else:
        st.info("No attacks yet. Hit ACTIVATE HONEYPOT to test.")

st.divider()
st.caption("Test: Open /admin URL after clicking button above")
