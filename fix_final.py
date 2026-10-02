import re

with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Fix the batch prompt to be strict and professional again
old_prompt = "The client runs a broad, multi-category site. Find ANY creative angle to match these queries to ANY of the client's topics. Be EXTREMELY lenient and try to find matches even if loosely related. Return ONLY a comma-separated list of the numbers (e.g. 0, 5, 12) of up to 8 matching queries. You MUST select at least 1 query no matter what, even if it is a huge stretch. Do NOT return empty. Return at least one index."
new_prompt = "Carefully review these queries. Only select a query if the client's niche is a GENUINE and VALUABLE fit. Do not force a connection if it doesn't make sense. Return ONLY a comma-separated list of the numbers (e.g. 0, 5, 12) of up to 8 matching queries. If none are a good fit, return an empty string."
c = c.replace(old_prompt, new_prompt)

# 2. Fix the subject line logic
old_subject_logic = '''                    words = item['query'].split()
                    short_topic = " ".join(words[:4]).replace("?", "").replace('"', '')
                    natural_subject = f"Quick thought on your query regarding {short_topic}..."'''

new_subject_logic = '''                    import re
                    match = re.search(r'Summary:\s*(.+?)(?:\\r|\\n|$)', item['query'])
                    if match:
                        clean_summary = match.group(1).strip()[:60]
                        natural_subject = f"Re: Your query on {clean_summary}"
                    else:
                        natural_subject = "Quick thought on your recent media query"'''
c = c.replace(old_subject_logic, new_subject_logic)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed batch prompt and subject line')
