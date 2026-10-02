with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    'log_pitch_to_db("SYSTEM LOG", "Error in Pitch", str(e), "ERROR")',
    'log_pitch_to_db("SYSTEM LOG", "Error in Pitch", str(e), "ERROR", "ERROR")'
)

c = c.replace(
    'log_pitch_to_db("SYSTEM LOG", "Pitch Gen", f"Starting AI generation for index {idx}", "LOG")',
    'log_pitch_to_db("SYSTEM LOG", "Pitch Gen", f"Starting AI generation for index {idx}", "LOG", "LOG")'
)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed arguments')
