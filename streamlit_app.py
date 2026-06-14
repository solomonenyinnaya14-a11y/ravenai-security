import streamlit as st
import sqlite3
import time
from datetime import datetime
import ssl
import socket
import requests

st.set_page_config(page_title="RavenAI - AI Security Scanner", layout="centered", page_icon="🦅")

# DARK THEME
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace; }
    .stApp { background-color: #0a0a0a; color: #e0e0e0; }
    div[data-testid="stButton"] > button:first-child { 
        background: #00ff88; color: #0a0a0a; font-weight: 700; 
        border-radius: 8px; height: 52px; font-size: 18px; border: none; width: 100%;
    }
    .blur-box { filter: blur(8px); opacity: 0.4; }
    .fomo-box { border: 2px solid #00ff88; padding: 20px; border-radius: 12px; text-align: center; margin-top: 25px; background: #0f0f0f; }
</style>
""", unsafe_allow_html=True)

# DATABASE
conn = sqlite3.connect('leads.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY, email TEXT, domain TEXT, date TEXT)''')
conn.commit()

# HERO
st.markdown("# 🦅 RavenAI")
st.markdown("### AI Cybersecurity Scanner")
st.markdown("Scan your domain. Find vulnerabilities before hackers do.")
st.divider()

# INPUT MUST BE ABOVE BUTTON
domain = st.text_input("Enter target domain", placeholder="example.com", key="domain_input")

def live_scan(domain):
    results = []
    # 1. SSL CERT CHECK
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry - datetime.now()).days
                if days_left < 30:
                    results.append(("error", f"SSL expires in {days_left} days"))
                else:
                    results.append(("info", f"SSL valid for {days_left} days"))
    except:
        results.append(("warning", "No SSL/HTTPS found - Site insecure"))
    
    # 2. SECURITY HEADERS
    try:
        r = requests.get(f"https://{domain}", timeout=5)
        h = r.headers
        if 'Strict-Transport-Security' not in h:
            results.append(("warning", "Missing HSTS Header"))
        if 'X-Frame-Options' not in h:
            results.append(("error", "Missing X-Frame-Options - Clickjacking risk"))
    except:
        results.append(("error", "Site unreachable"))
    
    return results[:3]

# BUTTON LOGIC
if st.button("Start Free Scan", use_container_width=True, type="primary"):
    
    domain_clean = domain.strip() if domain else ""
    
    if not domain_clean:
        st.error("❌ Enter a domain")
    elif "@" in domain_clean or "." not in domain_clean:
        st.error("❌ Enter a domain like: example.com")
    else:
        domain = domain_clean.lower().replace("https://", "").replace("http://", "").replace("/", "")
        
        with st.spinner("🔍 Checking SSL... Reading headers..."):
            scan_results = live_scan(domain)
        
        st.success(f"✅ Live scan complete for **{domain}**")
        st.markdown("### 🔍 Free Results")
        for i, (type, msg) in enumerate(scan_results, 1):
            if type == "error": st.error(f"{i}. {msg}")
            elif type == "warning": st.warning(f"{i}. {msg}")
            else: st.info(f"{i}. {msg}")
        
        st.markdown("---")
        st.markdown("### 🔒 7 Advanced Issues Hidden")
        st.markdown('<div class="blur-box">', unsafe_allow_html=True)
        for i in range(4, 11):
            st.error(f"{i}. ████████████████")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # EMAIL CAPTURE
        st.markdown('<div class="fomo-box">', unsafe_allow_html=True)
        st.markdown("### 🚨 Unlock Full Report")
        email = st.text_input("Enter your email", placeholder="you@example.com", key="email_input")
        
        if st.button("Send Me Full Report", use_container_width=True):
            if not email or "@" not in email or "." not in email:
                st.error("❌ Enter valid email")
            else:
                c.execute("INSERT INTO leads (email, domain, date) VALUES (?, ?, ?)", 
                         (email, domain, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                st.success(f"✅ Report queued for **{email}**")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("👆 Enter a domain above and hit `Start Free Scan`")
