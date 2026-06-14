import streamlit as st
import sqlite3
import time
from datetime import datetime

st.set_page_config(page_title="RavenAI - AI Security Scanner", layout="centered", page_icon="🦅")

# DARK HACKER THEME
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace; }
    .stApp { background-color: #0a0a0a; color: #e0e0e0; }
    
    div[data-testid="stButton"] > button:first-child { 
        background: #00ff88; color: #0a0a0a; font-weight: 700; 
        border-radius: 8px; height: 52px; font-size: 18px; border: none;
        width: 100%;
    }
    div[data-testid="stButton"] > button:first-child:hover { 
        background: #00cc6a; transform: scale(1.02);
    }
    
    .stTextInput input { 
        background-color: #1a1a1a; color: #00ff88; 
        border: 1px solid #333; border-radius: 6px; font-size: 16px;
    }
    
    .blur-box { 
        filter: blur(8px); opacity: 0.4; user-select: none; 
    }
    
    .fomo-box { 
        border: 2px solid #00ff88; padding: 20px; border-radius: 12px; 
        text-align: center; margin-top: 25px; background: #0f0f0f;
    }
</style>
""", unsafe_allow_html=True)

# DATABASE
conn = sqlite3.connect('leads.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS leads 
             (id INTEGER PRIMARY KEY, email TEXT, domain TEXT, date TEXT)''')
conn.commit()

# HERO
st.markdown("# 🦅 RavenAI")
st.markdown("### AI Cybersecurity Scanner")
st.markdown("Scan your domain. Find vulnerabilities before hackers do.")
st.markdown("**Powered by AI • No signup • Instant results**")
st.divider()

# INPUT
domain = st.text_input("Enter target domain", placeholder="example.com", key="domain_input")

if st.button("Start Free Scan", use_container_width=True, type="primary"):
    
    # FIXED VALIDATION - NO SPACE QUOTES ANYMORE
    domain_clean = domain.strip() if domain else ""
    
    if not domain_clean:
        st.error("❌ Enter a domain")
    elif "@" in domain_clean or "." not in domain_clean:
        st.error("❌ Enter a domain like: example.com")
    else:
        domain = domain_clean.lower().replace("https://", "").replace("http://", "").replace("/", "")
        
        # FAKE SCAN ANIMATION
        with st.spinner("🔍 Scanning ports... Checking headers... Analyzing SSL..."):
            time.sleep(3)
        
        st.success(f"✅ Scan complete for **{domain}**")
        
        # FREE RESULTS
        st.markdown("### 🔍 Free Results")
        st.error("1. Open Port 22 - SSH exposed to internet")
        st.warning("2. Missing HSTS Header - Clickjacking risk") 
        st.info("3. SSL Certificate expires in 30 days")
        
        st.markdown("---")
        st.markdown("### 🔒 7 Critical Issues Hidden")
        
        # BLUR + ████ FALLBACK
        st.markdown('<div class="blur-box">', unsafe_allow_html=True)
        for i in range(4, 11):
            st.error(f"{i}. ████████████████")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # EMAIL CAPTURE
        st.markdown('<div class="fomo-box">', unsafe_allow_html=True)
        st.markdown("### 🚨 Unlock Full Report")
        st.markdown("Get all 10 vulnerabilities + step-by-step fix recommendations")
        st.markdown("**Free for first 100 users • No spam**")
        
        email = st.text_input("Enter your email", placeholder="you@example.com", key="email_input")
        
        if st.button("Send Me Full Report", use_container_width=True):
            if not email or "@" not in email or "." not in email:
                st.error("❌ Enter valid email")
            else:
                c.execute("INSERT INTO leads (email, domain, date) VALUES (?, ?, ?)", 
                         (email, domain, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                st.success(f"✅ Report queued for **{email}**")
                st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("👆 Enter a domain above and hit `Start Free Scan`")

st.markdown("---")
st.caption("RavenAI v1.0 • Port Harcourt, NG")
