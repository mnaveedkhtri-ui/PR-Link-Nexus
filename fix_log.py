with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("result_str = res.choices[0].message.content", "result_str = res.choices[0].message.content\n            log_pitch_to_db('SYSTEM LOG', 'AI Result', result_str, 'LOG', 'LOG')")

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed log')
