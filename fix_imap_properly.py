with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# We will just replace the exact body of fetch_live_queries_from_haro using ast or simple replacement.
# Let's just find where it starts and ends cleanly.
start_sig = "def fetch_live_queries_from_haro(email_addr, app_password):"
end_sig = "def scrape_website_text(url: str) -> str:"

idx1 = c.find(start_sig)
idx2 = c.find(end_sig)

new_func = '''def fetch_live_queries_from_haro(email_addr, app_password):
    queries = []
    logs = ["> [*] CONNECTING TO INBOX FOR HARO/CONNECTIVELY EMAILS..."]
    try:
        import imaplib
        import email
        from email.header import decode_header
        
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_addr, app_password)
        mail.select("inbox")
        
        # Search all emails, we will check the last 15
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        
        if not email_ids:
            logs.append("> [*] No emails found in inbox.")
            return queries, logs
            
        found_haro = False
        import re
        for i in range(1, min(16, len(email_ids) + 1)):
            latest_email_id = email_ids[-i]
            status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    body = get_text_from_email(msg)
                    
                    if "Media Outlet:" in body or "Summary:" in body or "Connectively" in body or "HARO" in body:
                        found_haro = True
                        blocks = body.split("-----------------------------------")
                        if len(blocks) < 3:
                            blocks = body.split("Summary:")
                            
                        for block in blocks:
                            outlet = "HARO/Connectively"
                            if "Media Outlet:" in block:
                                try:
                                    outlet = block.split("Media Outlet:")[1].split("\\n")[0].strip()
                                except: pass
                            
                            if "Email:" in block or "@" in block or "Query:" in block or len(block) > 100:
                                q_text = block[:1000].strip()
                                emails_in_block = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+', block)
                                target_email = emails_in_block[0] if emails_in_block else None
                                
                                if target_email and len(q_text) > 50:
                                    queries.append({
                                        "title": q_text[:100].replace("\\n", " "),
                                        "outlet": outlet,
                                        "query": q_text,
                                        "name": "Journalist",
                                        "email": target_email
                                    })
                        break
            if found_haro:
                break
                
        if not found_haro:
            logs.append("> [*] Checked last 15 emails. No HARO/Connectively queries found.")
        else:
            logs.append(f"> [*] Extracted {len(queries)} queries from the latest PR email!")
    except Exception as e:
        logs.append(f"> [*] IMAP Error reading emails: {e}")
        
    return queries, logs

'''

c = c[:idx1] + new_func + c[idx2:]

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Replaced robustly')
