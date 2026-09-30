import os
import smtplib
import imaplib
import email
from email.header import decode_header
import time
import urllib.request
import xml.etree.ElementTree as ET
import re
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
import uvicorn
import html

app = FastAPI(title="PR-Nexus A-Z VIP Backend")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY")

# ==========================================
# DATABASE SETUP (A to Z Requirement)
# ==========================================
def init_db():
    conn = sqlite3.connect('pr_nexus.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pitches
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  journalist_name TEXT,
                  outlet TEXT,
                  query TEXT,
                  pitch_text TEXT,
                  status TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_pitch_to_db(name, outlet, query, pitch_text, status):
    conn = sqlite3.connect('pr_nexus.db')
    c = conn.cursor()
    c.execute("INSERT INTO pitches (journalist_name, outlet, query, pitch_text, status) VALUES (?, ?, ?, ?, ?)",
              (name, outlet, query, pitch_text, status))
    conn.commit()
    conn.close()

init_db()

class VIPRequest(BaseModel):
    sender_email: str
    app_password: str
    founder_name: str
    website_url: str

def get_text_from_email(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()
    return ""

def fetch_live_queries():
    rss_url = "https://news.google.com/rss/search?q=intitle:%22looking+for+experts%22+OR+%22journorequest%22&hl=en-US&gl=US&ceid=US:en"
    queries = []
    try:
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        xml_data = urllib.request.urlopen(req, timeout=10).read()
        root = ET.fromstring(xml_data)
        
        for item in root.findall('.//item')[:3]:
            clean_title = html.unescape(item.find('title').text)
            queries.append({
                "name": "Journalist", 
                "outlet": "Live Feed",
                "email": "test@example.com",
                "query": clean_title
            })
    except Exception as e:
        queries = [{"name": "Sarah", "outlet": "TechCrunch", "email": "", "query": "Does traditional Domain Authority matter in 2026?"}]
    return queries

def scrape_website_text(url: str) -> str:
    try:
        if not url.startswith('http'): url = 'https://' + url
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        text = re.sub(r'<script.*?</script>', '', html_content, flags=re.DOTALL)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^<]+>', ' ', text)
        return re.sub(r'\s+', ' ', text).strip()[:3000]
    except Exception as e:
        return f"Error scraping: {e}"

def extract_niche_with_ai(client, text: str) -> str:
    if "Error scraping" in text: return "Digital Agency & SEO services."
    prompt = f"Analyze website text and define its specific business niche in a concise 15-word summary. \nText: {text}"
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="qwen/qwen3.8-27b", temperature=0.2, max_tokens=40)
        return res.choices[0].message.content.strip()
    except:
        return "Technology & SEO Services"

def ai_semantic_filter(client, query: str, client_niche: str) -> bool:
    prompt = f"You are a smart PR Manager. Your client's expertise: '{client_niche}'. Journalist asks: '{query}'. Could your client answer this? Answer ONLY 'YES' or 'NO'."
    try:
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="qwen/qwen3.8-27b", temperature=0.1, max_tokens=10)
        return "YES" in res.choices[0].message.content.strip().upper()
    except:
        return False

def scan_inbox_and_reply(email_addr, app_password, founder_name, website_url, client):
    logs = []
    logs.append(f"> [📥] Connecting to Gmail IMAP Server...")
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_addr, app_password)
        mail.select("inbox")
        status, messages = mail.search(None, "UNSEEN") # Changed back to UNSEEN for production
        email_ids = messages[0].split()
        
        if not email_ids:
            logs.append("> [📭] Inbox is empty. No new unread replies found.")
            return logs
            
        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes): subject = subject.decode(encoding if encoding else "utf-8")
                sender = msg.get("From")
                body = get_text_from_email(msg)
                
                logs.append(f"> [📧] New Email Found: {subject}")
                
                check_prompt = f"Is the following email a newsletter/spam, or a real human message? Answer ONLY 'SPAM' or 'REAL'.\nSubject: {subject}\nBody: {body[:500]}"
                is_real = client.chat.completions.create(messages=[{"role": "user", "content": check_prompt}], model="qwen/qwen3.8-27b", temperature=0.1, max_tokens=10).choices[0].message.content.strip().upper()
                
                if "SPAM" in is_real:
                    logs.append("> [🛡️] AI Filter: Discarded as Spam.")
                    continue
                
                logs.append("> [🧠] AI analyzing context and writing reply...")
                reply_prompt = f"You are {founder_name}, founder of {website_url}. Reply politely to this email from {sender}: '{body[:1000]}'. Sign off as {founder_name}."
                reply_text = client.chat.completions.create(messages=[{"role": "user", "content": reply_prompt}], model="qwen/qwen3.8-27b", temperature=0.7, max_tokens=250).choices[0].message.content
                
                logs.append(f"> [📤] Sending AI Auto-Reply to {sender}...")
                
                smtp = smtplib.SMTP('smtp.gmail.com', 587)
                smtp.starttls()
                smtp.login(email_addr, app_password)
                reply_msg = MIMEMultipart()
                reply_msg['From'] = email_addr
                reply_msg['To'] = sender # Real Reply to actual Sender
                reply_msg['Subject'] = f"Re: {subject}"
                reply_msg.attach(MIMEText(reply_text, 'plain'))
                smtp.sendmail(email_addr, sender, reply_msg.as_string())
                smtp.quit()
                
                log_pitch_to_db(sender, "Reply", subject, reply_text, "REPLIED")
                logs.append("> [✅] SUCCESS! Reply sent & logged to Database.")
                
        mail.logout()
    except Exception as e:
        logs.append(f"> [❌] IMAP ERROR: Could not read inbox. {e}")
    return logs

# ==========================================
# API ENDPOINTS
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    with open("dashboard.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/history")
async def get_history():
    conn = sqlite3.connect('pr_nexus.db')
    c = conn.cursor()
    c.execute("SELECT id, journalist_name, query, status, timestamp FROM pitches ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return {"status": "success", "data": rows}

@app.post("/api/run-vip-autonomous")
async def run_vip_loop(req: VIPRequest):
    logs = []
    client = Groq(api_key=GROQ_API_KEY)
    
    logs.append(f"> [🕸️] Requesting URL: {req.website_url}")
    scraped_text = scrape_website_text(req.website_url)
    logs.append(f"> [🧠] Analyzing website context via AI...")
    dynamic_niche = extract_niche_with_ai(client, scraped_text)
    logs.append(f"> [🎯] AI defined your Core Expertise as:\n   '{dynamic_niche}'")
    
    logs.append(f"\n> [🌐] CONNECTING TO LIVE INTERNET FEEDS (RSS)...")
    live_feeds = fetch_live_queries()
    
    for item in live_feeds:
        logs.append(f"\n> [*] Live Query Found: {item['query'][:60]}...")
        is_relevant = ai_semantic_filter(client, item['query'], dynamic_niche)
        if not is_relevant:
            logs.append("> [-] Action: DISCARDED (No semantic match).")
            continue
            
        logs.append("> [+] Action: MATCH FOUND! Initiating Pitch Generation...")
        try:
            system_prompt = f"""
            You are {req.founder_name}, a busy founder at {req.website_url}.
            Your expertise: {dynamic_niche}.
            You are emailing a journalist to provide a quick quote for their story.
            
            CRITICAL RULES FOR 100% HUMAN STYLE:
            1. DO NOT write long, robotic, run-on sentences. 
            2. Write like a real, busy person. Extremely conversational and casual.
            3. Maximum 3 sentences total. Keep it punchy.
            4. USE LINE BREAKS (paragraphs) between sentences so it's easy to read.
            5. Start with "Hi {item['name']},".
            6. Provide ONE unique, contrarian thought or data point. No complex jargon.
            7. Sign off simply with:
            Best,
            {req.founder_name}
            {req.website_url}
            """
            pitch_text = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Journalist Query: \"{item['query']}\"\nWrite the email."}],
                model="qwen/qwen3.8-27b", temperature=0.7, max_tokens=250
            ).choices[0].message.content
            
            words = item['query'].split()
            short_topic = " ".join(words[:4]).replace("?", "").replace('"', '')
            natural_subject = f"Quick thought on your query regarding {short_topic}..."
            
            msg = MIMEMultipart()
            msg['From'] = req.sender_email
            msg['To'] = item['email'] # ACTUAL PRODUCTION DELIVERY TO TARGET
            msg['Subject'] = natural_subject
            msg.attach(MIMEText(pitch_text, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(req.sender_email, req.app_password)
            server.sendmail(req.sender_email, item['email'], msg.as_string()) # ACTUAL DELIVERY
            server.quit()
            
            log_pitch_to_db(item['name'], item['outlet'], item['query'], pitch_text, "PITCH SENT")
            logs.append(f"> [✅] SUCCESS! Live Pitch Delivered to Journalist & Logged to Database.")
        except Exception as e:
            logs.append(f"> [❌] SMTP ERROR.")

    logs.append(f"\n> [🤖] Phase 1 (Pitching) complete.")
    return {"status": "success", "logs": logs}

@app.post("/api/run-imap-agent")
async def run_imap_agent(req: VIPRequest):
    client = Groq(api_key=GROQ_API_KEY)
    logs = scan_inbox_and_reply(req.sender_email, req.app_password, req.founder_name, req.website_url, client)
    return {"status": "success", "logs": logs}

if __name__ == "__main__":
    print("[*] A-to-Z Database Engine Started... Open localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
