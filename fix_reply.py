with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_logic = '''                sender = msg.get("From")
                body = get_text_from_email(msg)'''

new_logic = '''                sender = msg.get("From")
                
                # SECURITY FILTER: Don't reply to random spam/newsletters
                sender_lower = str(sender).lower()
                if "no-reply" in sender_lower or "amazon" in sender_lower or "newsletter" in sender_lower or "support" in sender_lower:
                    logs.append(f"> [*] Skipped automated/marketing email from {sender}")
                    continue
                    
                body = get_text_from_email(msg)'''

c = c.replace(old_logic, new_logic)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed inbox agent')
