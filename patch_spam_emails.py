import os

with open('main.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix 1: Filter out spam/generic emails from emails_in_block
old_target = """if e.lower() != email_addr.lower() and 'haro' not in e.lower() and 'connectively' not in e.lower():"""
new_target = """bad_prefixes = ['spam', 'noreply', 'no-reply', 'support', 'info', 'admin', 'hello', 'marketing', 'newsletter']
                                      is_bad = any(e.lower().startswith(b + '@') for b in bad_prefixes)
                                      if not is_bad and e.lower() != email_addr.lower() and 'haro' not in e.lower() and 'connectively' not in e.lower():"""

code = code.replace(old_target, new_target)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patch applied for spam prefix emails.")
