with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('async def run_vip_loop', 'def run_vip_loop')
c = c.replace('await run_vip_loop', 'run_vip_loop')
c = c.replace('async def run_imap_agent', 'def run_imap_agent')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed async blocking endpoints')
