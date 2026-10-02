import re

with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'print(f"> "); logs.append(f"> ' in line:
        content = line.split('logs.append(f"> ')[1]
        new_lines.append(line.split('print(f"> ");')[0] + f'print(f"> {content.strip()[:-1]}")\n')
        new_lines.append(line.split('print(f"> ");')[0] + f'logs.append(f"> {content}')
    elif 'print("> "); logs.append("> ' in line:
        content = line.split('logs.append("> ')[1]
        new_lines.append(line.split('print("> ");')[0] + f'print("> {content.strip()[:-1]}")\n')
        new_lines.append(line.split('print("> ");')[0] + f'logs.append("> {content}')
    elif 'print(f"\\n> "); logs.append(f"\\n> ' in line:
        content = line.split('logs.append(f"\\n> ')[1]
        new_lines.append(line.split('print(f"\\n> ");')[0] + f'print(f"\\n> {content.strip()[:-1]}")\n')
        new_lines.append(line.split('print(f"\\n> ");')[0] + f'logs.append(f"\\n> {content}')
    else:
        new_lines.append(line)

with open('main.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Fixed properly')
