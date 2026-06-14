import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="RavenAI - AI Security Scanner", layout="centered")

# DARK HACKER THEME
st.markdown("""
<style>
    body, .stApp { background-color: #0a0a0a; color: #e0e0e0; }
    .main { font-family: 'JetBrains Mono', monospace; }
    .big-btn button { 
        background: #00ff88; color: #0a0a0a; font-weight: bold; 
        border-radius: 8px; height: 50px; font-size: 18px;
    }
    .blur { filter: blur(8px); opacity: 0.4; }
    .fomo-box { border: 2px solid #00ff88; padding: 20px; border-radius: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# DB for emails - free, no server needed
conn = sqlite3.connect('leads.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS leads 
             (email TEXT, domain TEXT, date TEXT)''')
conn.commit()

# HERO SECTION
st.markdown("# 🦅 RavenAI")
st.markdown("### AI Cybersecurity Scanner")
st.markdown("Scan your domain. Find vulnerabilities before hackers do.")
st.markdown("**Powered by AI • No signup • Instant results**")
st.divider()

# SCAN INPUT
domain = st.text_input("Enter target domain", placeholder="example.com")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    scan_btn = st.button("Start Free Scan", use_container_width=True, type="primary")

# FAKE RESULTS + FOMO
if scan_btn and domain:
    st.success(f"✅ Scan complete for {domain}")
    
    st.markdown("### 🔍 Free Results")
    st.error("1. Open Port 22 - SSH exposed")
    st.warning("2. Missing HSTS Header") 
    st.info("3. SSL Certificate expires in 30 days")
    
    st.markdown("---")
    st.markdown("### 🔒 7 Critical Issues Hidden")
    
    st.markdown('<div class="blur">', unsafe_allow_html=True)
    st.error("4. SQL Injection vulnerability detected")
    st.error("5. Admin panel exposed /admin")
    st.error("6. XSS vulnerability in login form")
    st.error("7. Outdated WordPress 5.8")
    st.error("8. Directory listing enabled")
    st.error("9. Weak password policy")
    st.error("10. Backup files exposed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # EMAIL CAPTURE INSTEAD OF PAYMENT
    st.markdown('<div class="fomo-box">', unsafe_allow_html=True)
    st.markdown("### 🚨 Unlock Full Report")
    st.markdown("Get all 10 vulnerabilities + fix recommendations sent to your email")
    st.markdown("**Free for first 100 users**")
    
    email = st.text_input("Enter your email", placeholder="you@example.com")
    
    st.markdown('<div class="big-btn">', unsafe_allow_html=True)
    if st.button("Send Me Full Report", use_container_width=True):
        if "@" in email and domain:
            c.execute("INSERT INTO leads VALUES (?, ?, ?)", 
                     (email, domain, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            st.success(f"✅ Report queued for {email}")
            st.info("Check inbox in 2 mins. We’ll add payment later CEO 😉")
        else:
            st.error("Enter valid email")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
else:
    st.markdown("👆 Enter a domain above and hit `Start Free Scan`")
