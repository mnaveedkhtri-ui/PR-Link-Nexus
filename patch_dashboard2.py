with open('dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
# Remove name field div
c = re.sub(r'<div>\s*<label class="block text-sm font-medium text-gray-400 mb-2">Your Full Name</label>\s*<input type="text" id="founder_name".*?</div>', '', c, flags=re.DOTALL)
# Fix the title from "2. Zero-Click Target" to just "Target Configuration"
c = c.replace('2. Zero-Click Target', 'Target Configuration')
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Dashboard patched 2.')
