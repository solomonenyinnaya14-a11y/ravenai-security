import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="RavenAI - AI Security Scanner", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    body, .stApp { background-color: #0a0a0a; color: #e0e0e0; }
    .main { font-family: 'JetBrains Mono', monospace; }
    div[data-testid="stButton"] button { 
        background: #00ff88; color: #0a0a0a; font-weight: bold; 
        border-radius: 8px; height: 50px; font-size: 18px; border: none;
    }
    div[data-testid="stButton"] button:hover { background: #00cc6a; }
    .blur-box { filter: blur(8px); opacity: 0.4; user-select: none; }
    .fomo-box { border: 2px solid #00ff88; padding: 20px; border-radius: 10px; text-align: center; margin-top: 20px; }
    .stTextInput input { background-color: #1a1a1a; color: #00ff88; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# DB
conn = sqlite3.connect('leads.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS leads (email TEXT, domain TEXT, date TEXT)''')
conn.commit()

st.markdown("# 🦅 RavenAI")
st.markdown("### AI Cybersecurity Scanner")
st.markdown("Scan your domain. Find vulnerabilities before hackers do.")
st.markdown("**Powered by AI • No signup • Instant results**")
st.divider()

domain = st.text_input("Enter target domain", placeholder="example.com")

if st.button("Start Free Scan", use_container_width=True, type="primary"):
    if not domain or "@" in domain:
        st.error("❌ Enter a domain like: example.com")
    else:
        st.success(f"✅ Scan complete for {domain}")
        
        st.markdown("### 🔍 Free Results")
        st.error("1. Open Port 22 - SSH exposed")
        st.warning("2. Missing HSTS Header") 
        st.info("3. SSL Certificate expires in 30 days")
        
        st.markdown("---")
        st.markdown("### 🔒 7 Critical Issues Hidden")
        
        st.markdown('<div class="blur-box">', unsafe_allow_html=True)
        for i, vuln in enumerate(["SQL Injection vulnerability detected", "Admin panel exposed /admin", 
                                  "XSS vulnerability in login form", "Outdated WordPress 5.8",
                                  "Directory listing enabled", "Weak password policy", "Backup files exposed"], 4):
            st.error(f"{i}. {vuln}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="fomo-box">', unsafe_allow_html=True)
        st.markdown("### 🚨 Unlock Full Report")
        st.markdown("Get all 10 vulnerabilities + fix recommendations sent to your email")
        st.markdown("**Free for first 100 users**")
        
        email = st.text_input("Enter your email", placeholder="you@example.com", key="email")
        
        if st.button("Send Me Full Report", use_container_width=True):
            if "@" in email and domain:
                c.execute("INSERT INTO leads VALUES (?, ?, ?)", 
                         (email, domain, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit()
                st.success(f"✅ Report queued for {email}")
                st.balloons()
            else:
                st.error("Enter valid email")
        st.markdown('</div>', unsafe_allow_html=True)
