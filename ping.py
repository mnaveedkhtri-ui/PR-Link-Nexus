import urllib.request
import json

url = 'https://pr-link-nexus-production.up.railway.app/api/run-vip-autonomous'
data = json.dumps({'sender_email': '', 'app_password': '', 'founder_name': '', 'website_url': ''}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    response = urllib.request.urlopen(req, timeout=180)
    result = json.loads(response.read().decode('utf-8'))
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f'Error: {e}')
