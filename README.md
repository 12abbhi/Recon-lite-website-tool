# 🌐 Recon-Lite - Website Information Tool (Python)

## 📌 Overview
Recon-Lite is a Python-based GUI tool used for gathering information about a website.  
It performs basic reconnaissance by collecting IP, WHOIS, DNS records, HTTP headers, and server details.

---

## 🚀 Features
- GUI-based interface (Tkinter)
- Domain to IP resolution
- WHOIS information lookup
- DNS records (A, MX, NS, TXT)
- HTTP headers & technology detection
- Website title extraction
- IP geolocation
- Save report functionality
- Multi-threaded execution

---

## 🛠️ Technologies Used
- Python
- Tkinter
- Socket Programming
- Requests Library
- Whois Module
- DNS Resolver
- Threading

---

## ⚙️ How It Works
1. Enter a domain or URL  
2. Click "Start Recon"  
3. Tool gathers:
   - IP Address  
   - WHOIS Info  
   - DNS Records  
   - HTTP Headers  
   - Server Location  
4. Results displayed in GUI  

---

## ▶️ How to Run

```bash
pip install requests python-whois dnspython
python recon_lite.py

🔐 Security Note
This tool is for educational purposes only. Do not use it on unauthorized targets.
