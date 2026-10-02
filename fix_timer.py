with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('await asyncio.sleep(14400)', 'await asyncio.sleep(600)')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed timer')
