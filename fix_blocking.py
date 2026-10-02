import re

with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the startup event
old_startup = '''@app.on_event("startup")
async def startup_event():
    asyncio.create_task(autonomous_24_7_loop())'''

new_startup = '''import threading

def background_worker():
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(autonomous_24_7_loop())

@app.on_event("startup")
async def startup_event():
    threading.Thread(target=background_worker, daemon=True).start()'''

c = c.replace(old_startup, new_startup)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed blocking')
