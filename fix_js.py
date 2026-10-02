with open('dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
c = c.replace('        };\n        }', '        }')

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed JS syntax')
