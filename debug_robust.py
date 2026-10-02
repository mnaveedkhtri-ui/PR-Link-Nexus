with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

debug_endpoint = '''@app.post("/api/debug-robust")
def debug_robust(req: VIPRequest):
    req_email = req.sender_email or os.getenv("SENDER_EMAIL")
    req_pw = req.app_password or os.getenv("APP_PASSWORD")
    queries, logs = fetch_live_queries_from_haro(req_email, req_pw)
    return {"logs": logs, "query_count": len(queries)}
'''

c = c.replace('if __name__ == "__main__":', debug_endpoint + '\nif __name__ == "__main__":')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Added robust debug')
