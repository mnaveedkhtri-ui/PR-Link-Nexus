import sys

with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "target_email = None" in line:
        # Re-indent the block
        lines[i]   = " " * 32 + "target_email = None\n"
        lines[i+1] = " " * 32 + "for e in emails_in_block:\n"
        lines[i+2] = " " * 36 + "if e.lower() != email_addr.lower() and 'haro' not in e.lower() and 'connectively' not in e.lower():\n"
        lines[i+3] = " " * 40 + "target_email = e\n"
        lines[i+4] = " " * 40 + "break\n"

with open('main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
