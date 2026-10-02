with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('- {req_name}', 'Best,\\n                    {req_name}')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed signoff')
