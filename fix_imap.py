with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace run_imap_agent to use background tasks and os.getenv fallbacks
old_imap = '''@app.post("/api/run-imap-agent")
def run_imap_agent(req: VIPRequest):
    client = Groq(api_key=GROQ_API_KEY)
    logs = scan_inbox_and_reply(req.sender_email, req.app_password, req.founder_name, req.website_url, client)
    return {"status": "success", "logs": logs}'''

new_imap = '''def process_imap_agent(req: VIPRequest):
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
    return {"status": "success", "logs": ["> [*] Inbox Scanner Started in Background!", "> [*] Auto-replying to interested journalists...", "> [*] Check the Database tab later to see sent replies!"]}'''

c = c.replace(old_imap, new_imap)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed IMAP Agent')
