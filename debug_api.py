with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

debug_endpoint = '''@app.post("/api/debug-vip")
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
'''

c = c.replace('if __name__ == "__main__":', debug_endpoint + '\nif __name__ == "__main__":')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Added debug endpoint')
