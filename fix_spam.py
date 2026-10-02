with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

import re

old = '''                msg = email.message_from_bytes(response_part[1])
                body = get_text_from_email(msg)'''

new = '''                msg = email.message_from_bytes(response_part[1])
                
                # SPAM PREVENTION: Check if we already processed this exact email
                import os
                message_id = str(msg.get("Message-ID"))
                if os.path.exists("processed_haros.txt"):
                    with open("processed_haros.txt", "r") as f:
                        if message_id in f.read():
                            continue # Skip already processed emails
                            
                with open("processed_haros.txt", "a") as f:
                    f.write(message_id + "\\n")
                    
                body = get_text_from_email(msg)'''

c = c.replace(old, new)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed loop spam')
