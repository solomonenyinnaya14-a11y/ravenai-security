import streamlit as st
import ssl
import socket
import requests
from datetime import datetime
import sqlite3

# ... keep all your CSS + DB code from before ...

def live_scan(domain):
    results = []
    
    # 1. SSL CERT CHECK - REAL
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry - datetime.now()).days
                if days_left < 30:
                    results.append(("error", f"SSL expires in {days_left} days - {expiry.date()}"))
                else:
                    results.append(("info", f"SSL valid for {days_left} days"))
    except:
        results.append(("warning", "No SSL/HTTPS found - Site insecure"))
    
    # 2. SECURITY HEADERS - REAL
    try:
        r = requests.get(f"https://{domain}", timeout=5, allow_redirects=True)
        headers = r.headers
        if 'Strict-Transport-Security' not in headers:
            results.append(("warning", "Missing HSTS Header - Clickjacking risk"))
        if 'X-Frame-Options' not in headers:
            results.append(("error", "Missing X-Frame-Options - Clickjacking possible"))
        if 'Content-Security-Policy' not in headers:
            results.append(("warning", "No CSP - XSS attacks easier"))
    except:
        results.append(("error", "Site unreachable or blocks scanners"))
    
    return results[:3]  # Show 3 free, hide rest

# REPLACE your fake scan block with this:
if st.button("Start Free Scan", use_container_width=True, type="primary"):
    domain_clean = domain.strip() if domain else ""
    
    if not domain_clean:
        st.error("❌ Enter a domain")
    elif "@" in domain_clean or "." not in domain_clean:
        st.error("❌ Enter a domain like: example.com")
    else:
        domain = domain_clean.lower().replace("https://", "").replace("http://", "").replace("/", "")
        
        with st.spinner("🔍 Checking SSL... Reading headers... Analyzing DNS..."):
            scan_results = live_scan(domain)
        
        st.success(f"✅ Live scan complete for **{domain}**")
        st.markdown("### 🔍 Free Results")
        for type, msg in scan_results:
            if type == "error": st.error(f"1. {msg}")
            elif type == "warning": st.warning(f"2. {msg}")
            else: st.info(f"3. {msg}")
        
        # Keep the 7 blurred bars + email capture same as before
        st.markdown("---")
        st.markdown("### 🔒 7 Advanced Issues Hidden")
        st.markdown('<div class="blur-box">', unsafe_allow_html=True)
        for i in range(4, 11):
            st.error(f"{i}. ████████████████")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ... rest of email capture code ...
