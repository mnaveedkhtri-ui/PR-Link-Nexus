import re

with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Broaden IMAP search to catch all HARO emails
c = c.replace('(FROM "haro@helpareporter.com")', '(SUBJECT "HARO")')

# 2. Strip all emojis from log lines to prevent any possible Unicode issues
c = re.sub(r'\[[\U0001f000-\U0003ffff]+.*?\]', '[*]', c) # Target corrupted emojis
c = c.replace('', '')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Cleaned up main.py')
