with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'logs.append(f"> [' in line and 'Requesting URL:' in line:
        new_lines.extend([
            '    req_email = req.sender_email or os.getenv("SENDER_EMAIL")\n',
            '    req_pw = req.app_password or os.getenv("APP_PASSWORD")\n',
            '    req_name = req.founder_name or os.getenv("FOUNDER_NAME")\n',
            '    import sqlite3\n',
            '    conn = sqlite3.connect("pr_nexus.db")\n',
            '    cursor = conn.cursor()\n',
            '    cursor.execute("SELECT active_url FROM settings WHERE id = 1")\n',
            '    row = cursor.fetchone()\n',
            '    conn.close()\n',
            '    db_url = row[0] if row and row[0] else ""\n',
            '    req_url = req.website_url or db_url or os.getenv("WEBSITE_URL")\n',
            '    if not req_email or not req_pw or not req_url:\n',
            '        logs.append("> [X] ERROR: Missing Credentials in Env Vars.")\n',
            '        return {"status": "error", "logs": logs}\n',
            line
        ])
    else:
        new_lines.append(line)

with open('main.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Fixed missing vars')
