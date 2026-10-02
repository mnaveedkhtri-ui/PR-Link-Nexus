with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == "import re" and not line.startswith("import re"):
        continue # skip indented 'import re'
    new_lines.append(line)

with open('main.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Fixed imports')
