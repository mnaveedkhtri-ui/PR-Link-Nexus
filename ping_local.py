import urllib.request
import json
url = 'http://127.0.0.1:8080/api/run-vip-autonomous'
data = json.dumps({'sender_email': '', 'app_password': '', 'founder_name': '', 'website_url': ''}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode('utf-8'))
    print(json.dumps(result, indent=2))
except Exception as e:
    import urllib.error
    if isinstance(e, urllib.error.HTTPError):
        print(e.read().decode())
    else:
        print(e)
