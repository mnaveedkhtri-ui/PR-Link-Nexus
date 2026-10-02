with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

old = 'if target_email and len(q_text) > 50:'
new = 'if target_email and len(q_text) > 50 and "No AI Pitches Considered" not in q_text and "No AI Pitches Considered" not in block:'

c = c.replace(old, new)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Added AI detector filter')
