with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Make the niche extractor broader
c = c.replace('define its specific business niche in a concise 15-word summary', 'define ALL the broad categories it covers (e.g., Tech, Lifestyle, Business, Health, Finance, General) in a concise 20-word summary, treating it as a multi-category site if applicable')

# Make the batch prompt even more lenient for multi-category sites
c = c.replace('Find ANY creative, out-of-the-box angle to match these queries to the client\'s niche. Be very lenient.', 'The client runs a broad, multi-category site. Find ANY creative angle to match these queries to ANY of the client\'s topics. Be EXTREMELY lenient and try to find matches even if loosely related.')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed niche logic')
