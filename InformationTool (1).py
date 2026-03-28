import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import whois
import dns.resolver
import socket
from datetime import datetime
import threading

# ====================== RECON FUNCTIONS ======================
def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return "N/A"

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            "Registrar": w.registrar or "N/A",
            "Created": str(w.creation_date[0])[:10] if isinstance(w.creation_date, list) else str(w.creation_date)[:10] or "N/A",
            "Expires": str(w.expiration_date[0])[:10] if isinstance(w.expiration_date, list) else str(w.expiration_date)[:10] or "N/A",
            "Name Servers": "\n".join(w.name_servers) if w.name_servers else "N/A",
            "Emails": ", ".join(w.emails) if w.emails else "N/A",
            "Organization": w.org or "N/A"
        }
    except:
        return {"Error": "WHOIS lookup failed"}

def get_dns_records(domain):
    records = {}
    types = ['A', 'MX', 'NS', 'TXT']
    for t in types:
        try:
            answers = dns.resolver.resolve(domain, t)
            records[t] = [str(r) for r in answers]
        except:
            records[t] = ["Not Found"]
    return records

def get_headers(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        r = requests.get(url, timeout=12, allow_redirects=True)
        title = "N/A"
        if "<title>" in r.text:
            title = r.text.split("<title>")[1].split("</title>")[0].strip()
        return {
            "Status": r.status_code,
            "Server": r.headers.get("Server", "N/A"),
            "Title": title,
            "Powered-By": r.headers.get("X-Powered-By", "N/A"),
            "Final URL": r.url
        }
    except:
        return {"Error": "Failed to connect"}

def get_geo(ip):
    try:
        r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=8)
        data = r.json()
        return f"{data.get('city','N/A')}, {data.get('region','N/A')}, {data.get('country_name','N/A')}"
    except:
        return "Location unavailable"

# ====================== START RECON ======================
def start_recon():
    target = entry.get().strip()
    if not target:
        messagebox.showwarning("Input Required", "Please enter a domain or URL!")
        return

    domain = target.replace("https://", "").replace("http://", "").split("/")[0]

    # Reset UI
    result_text.delete(1.0, tk.END)
    status_label.config(text="🔄 Gathering Intelligence...", fg="#facc15")
    progress.start(10)

    def recon():
        ip = get_ip(domain)
        whois_data = get_whois_info(domain)
        dns_data = get_dns_records(domain)
        headers = get_headers(target)
        geo = get_geo(ip)

        root.after(0, lambda: show_results(domain, ip, whois_data, dns_data, headers, geo))

    threading.Thread(target=recon, daemon=True).start()

def show_results(domain, ip, whois_data, dns_data, headers, geo):
    result_text.delete(1.0, tk.END)

    # Header
    result_text.insert(tk.END, f"🌐 WEBSITE RECON REPORT\n", "title")
    result_text.insert(tk.END, f"{'='*80}\n\n", "separator")

    result_text.insert(tk.END, f"Target Domain     : {domain}\n", "info")
    result_text.insert(tk.END, f"IP Address        : {ip}\n", "info")
    result_text.insert(tk.END, f"Server Location   : {geo}\n\n", "info")

    # WHOIS Section
    result_text.insert(tk.END, "📋 WHOIS INFORMATION\n", "section")
    result_text.insert(tk.END, "-"*50 + "\n", "separator")
    for key, value in whois_data.items():
        result_text.insert(tk.END, f"{key:15} : {value}\n", "normal")

    # DNS Section
    result_text.insert(tk.END, "\n📡 DNS RECORDS\n", "section")
    result_text.insert(tk.END, "-"*50 + "\n", "separator")
    for rectype, values in dns_data.items():
        result_text.insert(tk.END, f"{rectype:5} : {', '.join(values)}\n", "normal")

    # HTTP Headers
    result_text.insert(tk.END, "\n🔧 HTTP HEADERS & TECHNOLOGY\n", "section")
    result_text.insert(tk.END, "-"*50 + "\n", "separator")
    for key, value in headers.items():
        result_text.insert(tk.END, f"{key:15} : {value}\n", "normal")

    status_label.config(text="✅ Recon Completed Successfully", fg="#4ade80")
    progress.stop()

def save_report():
    content = result_text.get(1.0, tk.END).strip()
    if not content or content == "🌐 WEBSITE RECON REPORT":
        messagebox.showwarning("Empty", "No data to save. Run a scan first!")
        return
    try:
        filename = f"Recon_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Report saved as:\n{filename}")
    except:
        messagebox.showerror("Error", "Failed to save report")

# ====================== MODERN GUI ======================
root = tk.Tk()
root.title("🌐 Recon-lite - Website Information Tool")
root.geometry("1150x820")
root.configure(bg="#0a0f1c")

# Custom styles
style = ttk.Style()
style.theme_use("clam")

# Title
title_frame = tk.Frame(root, bg="#0a0f1c")
title_frame.pack(pady=25)

tk.Label(title_frame, text="🌐 RECON-LITE", font=("Helvetica", 28, "bold"),
         fg="#67e8f9", bg="#0a0f1c").pack()
tk.Label(title_frame, text="Website Intelligence & Recon Tool",
         font=("Helvetica", 12), fg="#94a3b8", bg="#0a0f1c").pack()

# Input Card
input_card = tk.Frame(root, bg="#1e2937", relief="flat", bd=0, highlightbackground="#334155", highlightthickness=2)
input_card.pack(pady=20, padx=80, fill="x", ipady=20)

tk.Label(input_card, text="Enter Domain or URL", font=("Helvetica", 13, "bold"),
         fg="#e2e8f0", bg="#1e2937").pack(pady=(10,5))

entry = tk.Entry(input_card, font=("Helvetica", 16), width=50, bg="#334155", fg="#e2e8f0",
                 insertbackground="#67e8f9", justify="center")
entry.pack(pady=10, ipady=8)
entry.insert(0, "google.com")

# Buttons
btn_frame = tk.Frame(root, bg="#0a0f1c")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="🚀 Start Recon", font=("Helvetica", 14, "bold"), bg="#22d3ee", fg="#0f172a",
          width=18, height=2, command=start_recon).grid(row=0, column=0, padx=20)

tk.Button(btn_frame, text="💾 Save Report", font=("Helvetica", 14, "bold"), bg="#64748b", fg="white",
          width=18, height=2, command=save_report).grid(row=0, column=1, padx=20)

# Progress
progress = ttk.Progressbar(root, length=900, mode='indeterminate', style="TProgressbar")
progress.pack(pady=10, padx=80)

status_label = tk.Label(root, text="Ready • Enter domain and click Start Recon",
                        font=("Helvetica", 11), fg="#94a3b8", bg="#0a0f1c")
status_label.pack(pady=8)

# Result Area with Tags
result_frame = tk.Frame(root, bg="#0a0f1c")
result_frame.pack(padx=80, pady=10, fill="both", expand=True)

result_text = scrolledtext.ScrolledText(result_frame, height=22, font=("Consolas", 11),
                                        bg="#1e2937", fg="#e2e8f0", wrap=tk.WORD)
result_text.pack(fill="both", expand=True)

# Text Tags for styling
result_text.tag_config("title", font=("Helvetica", 16, "bold"), foreground="#67e8f9")
result_text.tag_config("section", font=("Helvetica", 13, "bold"), foreground="#facc15")
result_text.tag_config("separator", foreground="#475569")
result_text.tag_config("info", foreground="#a5b4fc")
result_text.tag_config("normal", foreground="#e2e8f0")

# Footer
tk.Label(root, text="Mini Project • Website Recon-lite • Made with ❤️ for Ethical Recon",
         font=("Helvetica", 9), fg="#475569", bg="#0a0f1c").pack(side="bottom", pady=15)

root.mainloop()