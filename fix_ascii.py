import re

with open('main.py', 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

# Replace any tag that looks like > [...] with > [*]
c = re.sub(r'> \[[^A-Za-z0-9]\]', '> [*]', c)
c = re.sub(r'> \[[^\]]*\]', '> [*]', c)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed corrupted tags')
