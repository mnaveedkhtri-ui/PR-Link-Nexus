with open('dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
c = re.sub(r'<div class="bg-gray-800 rounded-xl p-6 shadow-xl border border-gray-700 mb-6">.*?<h3 class="text-xl font-bold text-gray-100 mb-4">1\. Connect Your Email</h3>.*?</div>', '', c, flags=re.DOTALL)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Dashboard patched.')
