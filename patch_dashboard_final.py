with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
# Remove the entire Connect Your Email block
html = re.sub(r'<div class=\"bg-slate-800 p-5 rounded-lg border border-slate-600 shadow-inner\">\s*<h2 class=\"text-lg font-semibold text-blue-300 mb-2\">1\. Connect Your Email</h2>.*?(<div class=\"bg-slate-800 p-5 rounded-lg border border-slate-600 shadow-inner\">\s*<h2 class=\"text-lg font-semibold text-blue-300 mb-2\">Target Configuration</h2>)', r'\1', html, flags=re.DOTALL)

# Remove the founderName div block inside Target Configuration
html = re.sub(r'<div>\s*<label class=\"block text-sm text-slate-300 mb-1\">Your Full Name</label>\s*<input id=\"founderName\".*?</div>', '', html, flags=re.DOTALL)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Fixed HTML')
