import os

with open('main.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix 1: Filter out user's own email from emails_in_block
old_target = """target_email = emails_in_block[0] if emails_in_block else None"""
new_target = """target_email = None
                                  for e in emails_in_block:
                                      if e.lower() != email_addr.lower() and 'haro' not in e.lower() and 'connectively' not in e.lower():
                                          target_email = e
                                          break"""
code = code.replace(old_target, new_target)

# Fix 2: Prevent scan_inbox_and_reply from replying to the user's own email address
old_reply_check = """sender_lower = str(sender).lower()
                if "no-reply" in sender_lower or "amazon" in sender_lower or "newsletter" in sender_lower or "support" in sender_lower:"""
new_reply_check = """sender_lower = str(sender).lower()
                if email_addr.lower() in sender_lower or "no-reply" in sender_lower or "amazon" in sender_lower or "newsletter" in sender_lower or "support" in sender_lower:"""
code = code.replace(old_reply_check, new_reply_check)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patch applied.")
