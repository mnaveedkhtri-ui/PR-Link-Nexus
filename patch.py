import os
import sqlite3

with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()
    
c = c.replace('logs.append(f\"> [??] Requesting URL: {req.website_url}\")', '''
    req_email = req.sender_email or os.getenv("SENDER_EMAIL")
    req_pw = req.app_password or os.getenv("APP_PASSWORD")
    req_name = req.founder_name or os.getenv("FOUNDER_NAME")
    conn = sqlite3.connect('pr_nexus.db')
    cursor = conn.cursor()
    cursor.execute("SELECT active_url FROM settings WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    db_url = row[0] if row and row[0] else ""
    req_url = req.website_url or db_url or os.getenv("WEBSITE_URL")
    if not req_email or not req_pw or not req_url:
        logs.append("> [X] ERROR: Missing Credentials in Env Vars.")
        return {"status": "error", "logs": logs}
    logs.append(f"> [!] Requesting URL: {req_url}")
'''.strip())
c = c.replace('scraped_text = scrape_website_text(req.website_url)', 'scraped_text = scrape_website_text(req_url)')
c = c.replace('live_feeds, haro_logs = fetch_live_queries_from_haro(req.sender_email, req.app_password)', 'live_feeds, haro_logs = fetch_live_queries_from_haro(req_email, req_pw)')
c = c.replace('You are {req.founder_name}, a busy founder at {req.website_url}.', 'You are {req_name}, a busy founder at {req_url}.')
c = c.replace('{req.founder_name}', '{req_name}')
c = c.replace('{req.website_url}', '{req_url}')
c = c.replace('msg[\'From\'] = req.sender_email', 'msg[\'From\'] = req_email')
c = c.replace('server.login(req.sender_email, req.app_password)', 'server.login(req_email, req_pw)')
c = c.replace('server.sendmail(req.sender_email, item[\'email\'], msg.as_string())', 'server.sendmail(req_email, item[\'email\'], msg.as_string())')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Patched successfully.')
