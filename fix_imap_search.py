with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the search logic to search for HARO or Connectively specifically
old_search = "status, messages = mail.search(None, 'ALL')"
new_search = "status, messages = mail.search(None, '(OR (SUBJECT \"HARO\") (SUBJECT \"Connectively\"))')"
c = c.replace(old_search, new_search)

# Replace the loop range to just check the last 3 HARO emails instead of 15 (since they are guaranteed to be HARO)
old_range = "for i in range(1, min(16, len(email_ids) + 1)):"
new_range = "for i in range(1, min(4, len(email_ids) + 1)):"
c = c.replace(old_range, new_range)

# Fix the logging string to be accurate
c = c.replace("> [*] Checked last 15 emails.", "> [*] Checked recent PR emails.")

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed IMAP search query')
