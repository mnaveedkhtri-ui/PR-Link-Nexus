import re
with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# I need to revert my stupid mistake and do it properly.
c = re.sub(r'print\(f"> "\); logs\.append\(f"> (.*?)\)', r'print(f"> \1"); logs.append(f"> \1")', c)
c = re.sub(r'print\("> "\); logs\.append\("> (.*?)\)', r'print("> \1"); logs.append("> \1")', c)
c = re.sub(r'print\(f"\\n> "\); logs\.append\(f"\\n> (.*?)\)', r'print(f"\n> \1"); logs.append(f"\n> \1")', c)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed logs for real')
