with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

import_statement = '''import os
from dotenv import load_dotenv
load_dotenv()'''

c = c.replace('import os', import_statement, 1)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Added dotenv')
