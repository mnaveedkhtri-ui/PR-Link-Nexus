with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

import re
c = c.replace('."");', '.");')
c = c.replace('."")', '.")')
c = c.replace('!"");', '!");')
c = c.replace('!"")', '!")')
c = c.replace('?"");', '?");')
c = c.replace('?"")', '?")')
c = c.replace('\n"");', '\n");')
c = c.replace('\n"")', '\n")')

# Let's just fix the double quotes globally if they are next to parenthesis
c = re.sub(r'""\)', r'")', c)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed syntax')
