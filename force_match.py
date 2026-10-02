with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Make the batch prompt strictly require at least 1 match
c = c.replace(
    'If absolutely none, return empty.',
    'You MUST select at least 1 query no matter what, even if it is a huge stretch. Do NOT return empty. Return at least one index.'
)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Forced AI to match')
