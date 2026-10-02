with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_prompt = "The client runs a high-quality multi-category blog covering Tech, Lifestyle, Business, and Health. Identify the top 2 to 3 most relevant queries where the client can provide a genuinely valuable and creative perspective. You must think outside the box to make a high-quality connection, but avoid total spam. Always aim to select at least 1-2 good queries. Return ONLY a comma-separated list of the numbers (e.g. 0, 5, 12)."
new_prompt = "The client runs a high-quality multi-category blog covering Tech, Lifestyle, Business, and Health. You MUST select EXACTLY 3 queries from the list that are the closest match, even if they are not perfect fits. Be highly creative in finding a unique angle to connect the client's niche to these 3 queries. DO NOT return an empty list. Return ONLY a comma-separated list of exactly 3 numbers (e.g. 0, 5, 12)."

c = c.replace(old_prompt, new_prompt)

# Add a cap to ensure we don't spam if AI hallucinates 10 numbers
c = c.replace("selected_indices = [int(i.strip()) for i in re.findall(r'\d+', result_str)]", "selected_indices = [int(i.strip()) for i in re.findall(r'\d+', result_str)][:3]")

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed batch prompt to force 3 pitches')
