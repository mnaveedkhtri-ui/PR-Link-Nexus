with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

target = '''            try:
                process_vip_loop(req)
                print("[*] 24/7 AUTO-PILOT FINISHED PITCHING. GOING TO SLEEP.")'''

replacement = '''            try:
                process_vip_loop(req)
                print("[*] 24/7 AUTO-PILOT PITCHING COMPLETE. NOW CHECKING INBOX FOR REPLIES...")
                process_imap_agent(req)
                print("[*] 24/7 AUTO-PILOT FINISHED ALL TASKS. GOING TO SLEEP.")'''

c = c.replace(target, replacement)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Added IMAP agent to 24/7 loop')
