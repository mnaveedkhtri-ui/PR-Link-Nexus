with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('logs.append(f"> ', 'print(f"> "); logs.append(f"> ')
c = c.replace('logs.append("> ', 'print("> "); logs.append("> ')
c = c.replace('logs.append(f"\\n> ', 'print(f"\\n> "); logs.append(f"\\n> ')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed logs')
