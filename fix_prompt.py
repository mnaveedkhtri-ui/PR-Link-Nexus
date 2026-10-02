with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_prompt = "Carefully review these queries. Only select a query if the client's niche is a GENUINE and VALUABLE fit. Do not force a connection if it doesn't make sense. Return ONLY a comma-separated list of the numbers (e.g. 0, 5, 12) of up to 8 matching queries. If none are a good fit, return an empty string."
new_prompt = "The client runs a high-quality multi-category blog covering Tech, Lifestyle, Business, and Health. Identify the top 2 to 3 most relevant queries where the client can provide a genuinely valuable and creative perspective. You must think outside the box to make a high-quality connection, but avoid total spam. Always aim to select at least 1-2 good queries. Return ONLY a comma-separated list of the numbers (e.g. 0, 5, 12)."

c = c.replace(old_prompt, new_prompt)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed prompt')
