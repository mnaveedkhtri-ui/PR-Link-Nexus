with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('qwen/qwen3.8-27b', 'llama3-70b-8192')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed model name')
