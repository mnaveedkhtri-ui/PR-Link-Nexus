with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('print(f"> "); ', '')
c = c.replace('print("> "); ', '')
c = c.replace('print(f"\\n> "); ', '')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Removed broken prints')
