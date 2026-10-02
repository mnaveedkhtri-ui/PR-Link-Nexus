with open('dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()
import re
c = re.sub(r'function getPayload\(\) \{.*?\}', '''function getPayload() {
            const urlElement = document.getElementById('website_url');
            const w = urlElement ? urlElement.value : "";
            return { sender_email: "", app_password: "", founder_name: "", website_url: w };
        }''', c, flags=re.DOTALL)
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(c)
