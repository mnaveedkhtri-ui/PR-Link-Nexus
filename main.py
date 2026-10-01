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
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
import uvicorn
import html
import asyncio

app = FastAPI(title="PR-Nexus A-Z VIP Backend")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY")

async def autonomous_24_7_loop():
    while True:
        email = os.getenv("SENDER_EMAIL")
        app_pw = os.getenv("APP_PASSWORD")
        name = os.getenv("FOUNDER_NAME")
        
        # 1. Try to get URL from DB (Frontend UI)
        conn = sqlite3.connect('pr_nexus.db')
        c = conn.cursor()
        c.execute("SELECT active_url FROM settings WHERE id = 1")
        row = c.fetchone()
        conn.close()
        
        url = row[0] if row and row[0] else os.getenv("WEBSITE_URL")
        
        if email and app_pw and name and url:
            print("[*] 24/7 AUTO-PILOT WAKING UP...")
            req = VIPRequest(
                sender_email=email,
                app_password=app_pw,
                founder_name=name,
                website_url=url
            )
            try:
                process_vip_loop(req)
                print("[*] 24/7 AUTO-PILOT FINISHED PITCHING. GOING TO SLEEP.")
            except Exception as e:
                print(f"[!] 24/7 AUTO-PILOT ERROR: {e}")
        else:
            print("[!] 24/7 AUTO-PILOT: Missing environment variables. Skipping.")
            
        # Sleep for 4 hours (14400 seconds) - perfect for catching 3 daily HARO emails
        await asyncio.sleep(14400)

import threading

def background_worker():
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(autonomous_24_7_loop())

@app.on_event("startup")
async def startup_event():
    threading.Thread(target=background_worker, daemon=True).start()

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
    
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (id INTEGER PRIMARY KEY, active_url TEXT)''')
    c.execute("INSERT OR IGNORE INTO settings (id, active_url) VALUES (1, '')")
    
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
    sender_email: str = ""
    app_password: str = ""
    founder_name: str = ""
    website_url: str = ""

def get_text_from_email(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()
    return ""

def fetch_live_queries_from_haro(email_addr, app_password):
    queries = []
    logs = ["> [*] CONNECTING TO INBOX FOR HARO/CONNECTIVELY EMAILS..."]
    try:
        import imaplib
        import email
        from email.header import decode_header
        
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_addr, app_password)
        mail.select("inbox")
        
        # Search all emails, we will check the last 10
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        
        if not email_ids:
            logs.append("> [*] No emails found in inbox.")
            return queries, logs
            
        # Look at the last 15 emails to find the latest HARO/Connectively newsletter
        found_haro = False
        for i in range(1, min(16, len(email_ids) + 1)):
            latest_email_id = email_ids[-i]
            status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    body = get_text_from_email(msg)
                    
                    # Simple check: Does it look like a PR query email?
                    if "Media Outlet:" in body or "Summary:" in body or "Connectively" in body or "HARO" in body:
                        found_haro = True
                        blocks = body.split("-----------------------------------")
                        # Some new formats use different dividers, fallback to regex if blocks are 1
                        if len(blocks) < 3:
                            # Try splitting by double newlines or Summary:
                            blocks = body.split("Summary:")
                            
                        for block in blocks:
                            outlet = "HARO/Connectively"
                            if "Media Outlet:" in block:
                                try:
                                    outlet = block.split("Media Outlet:")[1].split("\n")[0].strip()
                                except: pass
                            
                            # Add block to queries if it contains a query or if we split by Summary:
                            if "Email:" in block or "@" in block or "Query:" in block or len(block) > 100:
                                # Clean up block
                                q_text = block[:1000].strip()
                                # We need an email to send to
                                emails_in_block = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', block)
                                target_email = emails_in_block[0] if emails_in_block else None
                                
                                if target_email and len(q_text) > 50:
                                    queries.append({
                                        "title": q_text[:100].replace("\n", " "),
                                        "outlet": outlet,
                                        "query": q_text,
                                        "name": "Journalist",
                                        "email": target_email
                                    })
                        break # Stop checking older emails since we found the latest one
            if found_haro:
                break
                
        if not found_haro:
            logs.append("> [*] Checked last 15 emails. No HARO/Connectively queries found.")
        else:
            logs.append(f"> [*] Extracted {len(queries)} queries from the latest PR email!")
    except Exception as e:
        logs.append(f"> [*] IMAP Error reading emails: {e}")
        
    return queries, logs
# 2. FETCH FROM HARO (IMAP)
    live_feeds, haro_logs = fetch_live_queries_from_haro(req_email, req_pw)
    logs.extend(haro_logs)
    
    # 3. BATCH PROCESSING ENGINE (To prevent API Rate Limits & Timeouts)
    pitch_count = 0
    if live_feeds:
        logs.append(f"> [*] BATCH PROCESSING {len(live_feeds)} QUERIES IN ONE GO (Speed Optimization)...")
        
        # Prepare a numbered list of all queries
        queries_text = ""
        for idx, item in enumerate(live_feeds):
            queries_text += f"{idx}. {item['title'][:100]}\n"
            
        batch_prompt = f"Client Niche: '{dynamic_niche}'. Here are {len(live_feeds)} HARO queries:\n{queries_text}\nThe client runs a broad, multi-category site. Find ANY creative angle to match these queries to ANY of the client's topics. Be EXTREMELY lenient and try to find matches even if loosely related. Return ONLY a comma-separated list of the numbers (e.g. 0, 5, 12) of up to 8 matching queries. If absolutely none, return empty."
        
        try:
            res = client.chat.completions.create(messages=[{"role": "user", "content": batch_prompt}], model="qwen/qwen3.8-27b", temperature=0.3, max_tokens=30)
            result_str = res.choices[0].message.content
            # Extract numbers from the response
            selected_indices = [int(i.strip()) for i in re.findall(r'\d+', result_str)]
        except Exception as e:
            logs.append(f"> [*] Batch filter error: {e}")
            selected_indices = []
            
        logs.append(f"> [*] BATCH COMPLETE. AI selected {len(selected_indices)} creative matching queries!")
        
        for idx in selected_indices[:8]:  # Increased to 8 per run to guarantee 10+ daily pitches across 3 runs
            if idx < len(live_feeds):
                item = live_feeds[idx]
                logs.append(f"\n> [*] CREATIVE MATCH: {item['title'][:50]}... Initiating Pitch Generation...")
                
                try:
                    system_prompt = f"""
                    You are {req_name}, a busy founder at {req_url}.
                    Your expertise: {dynamic_niche}.
                    You are emailing a journalist to provide a quick quote for their story.
                    
                    CRITICAL RULES FOR 100% HUMAN STYLE:
                    1. Find a creative, unique angle connecting your expertise to their query.
                    2. Write like a real, busy person. Extremely conversational and casual.
                    3. Maximum 3 sentences total. Keep it punchy.
                    4. USE LINE BREAKS (paragraphs) between sentences so it's easy to read.
                    5. Start with "Hi {item['name']},".
                    6. Sign off simply with:
                    Best,
                    {req_name}
                    {req_url}
                    """
                    pitch_text = client.chat.completions.create(
                        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Journalist Query: \"{item['query']}\"\nWrite the email."}],
                        model="qwen/qwen3.8-27b", temperature=0.7, max_tokens=250
                    ).choices[0].message.content
                    
                    words = item['query'].split()
                    short_topic = " ".join(words[:4]).replace("?", "").replace('"', '')
                    natural_subject = f"Quick thought on your query regarding {short_topic}..."
                    
                    msg = MIMEMultipart()
                    msg['From'] = req_email
                    msg['To'] = item['email'] # ACTUAL HARO TARGET
                    msg['Subject'] = natural_subject
                    msg.attach(MIMEText(pitch_text, 'plain'))
                    
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(req_email, req_pw)
                    server.sendmail(req_email, item['email'], msg.as_string())
                    server.quit()
                    
                    log_pitch_to_db(item['name'], item['outlet'], item['query'], pitch_text, "PITCH SENT")
                    logs.append(f"> [*] SUCCESS! HARO Pitch Delivered to {item['email']} & Logged.")
                    pitch_count += 1
                except Exception as e:
                    logs.append(f"> [*] SMTP ERROR: {e}")

    logs.append(f"\n> [*] Phase 1 (Pitching) complete. Total Pitches Sent: {pitch_count}")
    return {"status": "success", "logs": logs}

class ClientSettings(BaseModel):
    website_url: str

@app.post("/api/set-active-client")
async def set_active_client(settings: ClientSettings):
    conn = sqlite3.connect('pr_nexus.db')
    c = conn.cursor()
    c.execute("UPDATE settings SET active_url = ? WHERE id = 1", (settings.website_url,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"24/7 Bot is now permanently pitching for: {settings.website_url}"}

@app.get("/api/get-active-client")
async def get_active_client():
    conn = sqlite3.connect('pr_nexus.db')
    c = conn.cursor()
    c.execute("SELECT active_url FROM settings WHERE id = 1")
    row = c.fetchone()
    conn.close()
    return {"website_url": row[0] if row and row[0] else ""}

def process_imap_agent(req: VIPRequest):
    client = Groq(api_key=GROQ_API_KEY)
    req_email = req.sender_email or os.getenv("SENDER_EMAIL")
    req_pw = req.app_password or os.getenv("APP_PASSWORD")
    req_name = req.founder_name or os.getenv("FOUNDER_NAME")
    
    import sqlite3
    conn = sqlite3.connect("pr_nexus.db")
    cursor = conn.cursor()
    cursor.execute("SELECT active_url FROM settings WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    db_url = row[0] if row and row[0] else ""
    req_url = req.website_url or db_url or os.getenv("WEBSITE_URL")
    
    scan_inbox_and_reply(req_email, req_pw, req_name, req_url, client)

@app.post("/api/run-imap-agent")
def run_imap_agent(req: VIPRequest, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(process_imap_agent, req)
    return {"status": "success", "logs": ["> [*] Inbox Scanner Started in Background!", "> [*] Auto-replying to interested journalists...", "> [*] Check the Database tab later to see sent replies!"]}

@app.post("/api/debug-vip")
def debug_vip(req: VIPRequest):
    client = Groq(api_key=GROQ_API_KEY)
    req_email = req.sender_email or os.getenv("SENDER_EMAIL")
    req_pw = req.app_password or os.getenv("APP_PASSWORD")
    req_url = req.website_url or os.getenv("WEBSITE_URL")
    
    logs = ["> [*] DEBUG STARTING..."]
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(req_email, req_pw)
        mail.select("inbox")
        status, messages = mail.search(None, '(SUBJECT "HARO")')
        email_ids = messages[0].split()
        if not email_ids:
            logs.append("> [*] DEBUG: No HARO emails found in inbox.")
            return {"logs": logs}
        logs.append(f"> [*] DEBUG: Found {len(email_ids)} HARO emails.")
        
        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                body = get_text_from_email(msg)
                logs.append(f"> [*] DEBUG: Email Body Length = {len(body)}")
                blocks = body.split("-----------------------------------")
                logs.append(f"> [*] DEBUG: Found {len(blocks)} blocks split by dashes.")
                
                queries = []
                for block in blocks:
                    if "Summary:" in block and "Email: " in block and "Query:" in block:
                        queries.append("Query Found")
                logs.append(f"> [*] DEBUG: Extracted {len(queries)} queries via strict matching.")
    except Exception as e:
        logs.append(f"> [*] DEBUG ERROR: {e}")
        
    return {"logs": logs}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[*] A-to-Z Database Engine Started... Open 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
