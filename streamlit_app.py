import streamlit as st
import requests
import uuid

# Load secrets
PAYSTACK_PUBLIC = st.secrets["PAYSTACK_PUBLIC"]
PAYSTACK_SECRET = st.secrets["PAYSTACK_SECRET"]
APP_URL = st.secrets["APP_URL"]
TELEGRAM_BOT_TOKEN = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID", "")

st.set_page_config(page_title="RavenAI", page_icon="🐦‍⬛", layout="centered")

# Session state
if "paid" not in st.session_state:
    st.session_state.paid = False
if "reference" not in st.session_state:
    st.session_state.reference = None

# Check if returning from Paystack
query_params = st.query_params
if "reference" in query_params and not st.session_state.paid:
    ref = query_params["reference"]
    st.session_state.reference = ref
    
    # Verify payment
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET}"}
    verify = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
    
    if verify.status_code == 200:
        data = verify.json()["data"]
        if data["status"] == "success":
            st.session_state.paid = True
            st.balloons()
            st.success(f"✅ Payment verified! Ref: {ref}")
            
            # Send Telegram alert
            if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
                msg = f"🚨 NEW CUSTOMER PAID!\nEmail: {data['customer']['email']}\nAmount: ₦{data['amount']/100}\nRef: {ref}"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                            json={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

# UI
st.title("🐦‍⬛ RavenAI - Honeypot-as-a-Service")
st.caption("Catch hackers. Collect intel. Get paid ₦5000/month")

if not st.session_state.paid:
    st.write("### Step 1: Unlock Hacker Logs")
    email = st.text_input("Your email", placeholder="ceo@ravenai.com")
    
    if st.button("Pay ₦5000 with Paystack", type="primary"):
        if not email:
            st.warning("Enter email first CEO")
        else:
            headers = {"Authorization": f"Bearer {PAYSTACK_SECRET}"}
            ref = f"RAVEN_{uuid.uuid4().hex[:8]}"
            data = {
                "email": email,
                "amount": 5000 * 100,  # ₦5000 = 500000 kobo. Paystack needs amount in kobo
                "currency": "NGN",  # Changed from USD to NGN for test mode
                "reference": ref,
                "callback_url": APP_URL,
                "metadata": {"product": "RavenAI Monthly"}
            }
            
            res = requests.post("https://api.paystack.co/transaction/initialize", 
                               headers=headers, json=data)
            
            if res.status_code == 200:
                auth_url = res.json()["data"]["authorization_url"]
                st.link_button("→ Complete Payment on Paystack", auth_url, type="primary")
                st.info("Test card: 4081 9482 1234 5678 | Expiry: 12/30 | CVV: 123 | PIN: 0000 | OTP: 123456")
            else:
                st.error(f"Error: {res.json()}")
else:
    st.write("### Step 2: Your Honeypot Dashboard 🐐")
    st.success("Access unlocked! RavenAI is watching for hackers now.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("SSH Attacks Today", "47", "+12")
    col2.metric("Countries Hit", "23", "+5") 
    col3.metric("Wallets Drained", "₦0", "Demo mode")
    
    st.write("---")
    st.code("""
    [2026-06-14 14:32:12] 185.220.101.45 → SSH root login attempt
    [2026-06-14 14:32:15] 185.220.101.45 → Tried password: admin123
    [2026-06-14 14:32:18] 185.220.101.45 → Downloaded malware.exe
    [2026-06-14 14:33:02] 45.142.212.100 → SQL injection probe
    """, language="log")
    
    st.download_button("Download Full Logs", "sample_hacker_log.txt", "raven_logs.txt")

st.sidebar.write("### RavenAI Status")
st.sidebar.write("Mode: 🧪 TEST NGN")
st.sidebar.write(f"Webhook: {APP_URL}")
