import re

with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Add BackgroundTasks to import
if 'BackgroundTasks' not in c:
    c = c.replace('from fastapi import FastAPI', 'from fastapi import FastAPI, BackgroundTasks')

# Rename old run_vip_loop to process_vip_loop
c = c.replace('@app.post("/api/run-vip-autonomous")\ndef run_vip_loop(req: VIPRequest):', 'def process_vip_loop(req: VIPRequest):')

# Create a new run_vip_loop that uses BackgroundTasks
new_endpoint = '''@app.post("/api/run-vip-autonomous")
def run_vip_loop(req: VIPRequest, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(process_vip_loop, req)
    return {"status": "success", "logs": ["> [*] Manual Request Accepted!", "> [*] Pitching engine has started in the background.", "> [*] Please wait 2-3 minutes, then check the 'Database & Reports' tab to see the live results!"]}
'''

# Insert the new endpoint before process_vip_loop
c = c.replace('def process_vip_loop(req: VIPRequest):', new_endpoint + '\ndef process_vip_loop(req: VIPRequest):')

# Fix the 24/7 loop to call process_vip_loop instead of run_vip_loop
c = c.replace('run_vip_loop(req)', 'process_vip_loop(req)')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed endpoints to use BackgroundTasks')
