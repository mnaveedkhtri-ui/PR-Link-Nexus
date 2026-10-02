with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

target = "logs.append(f\"\\n> [*] CREATIVE MATCH: {item['title'][:50]}... Initiating Pitch Generation...\")"
replacement = target + '''
                log_pitch_to_db("SYSTEM LOG", "Pitch Gen", f"Starting AI generation for index {idx}", "LOG")
'''
c = c.replace(target, replacement)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Added pre-generation logging')
