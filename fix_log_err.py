with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("logs.append(f\"> [*] Batch filter error: {e}\")", "logs.append(f\"> [*] Batch filter error: {e}\")\n            log_pitch_to_db('SYSTEM LOG', 'AI Filter Error', str(e), 'ERROR', 'ERROR')")

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed error log')
