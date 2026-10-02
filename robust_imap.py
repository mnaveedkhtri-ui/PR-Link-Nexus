with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# Find the fetch_live_queries_from_haro function and replace it
def_start = c.find('def fetch_live_queries_from_haro')
def_end = c.find('# 2. FETCH FROM HARO', def_start)

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
                                    outlet = block.split("Media Outlet:")[1].split("\\n")[0].strip()
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
                                        "title": q_text[:100].replace("\\n", " "),
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
'''

c = c[:def_start] + new_func + c[def_end:]

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Replaced fetch_live_queries_from_haro with robust version')
