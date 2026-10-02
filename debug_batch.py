import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))
batch_prompt = "The client runs a high-quality multi-category blog covering Tech, Lifestyle, Business, and Health. You MUST select EXACTLY 3 queries from the list that are the closest match, even if they are not perfect fits. Be highly creative in finding a unique angle to connect the client's niche to these 3 queries. DO NOT return an empty list. Return ONLY a comma-separated list of exactly 3 numbers (e.g. 0, 5, 12).\nQueries:\n1. Health tips\n2. Tech news\n3. Cooking\n4. Business\n5. Travel"
try:
    res = client.chat.completions.create(messages=[{"role": "user", "content": batch_prompt}], model="qwen/qwen3.8-27b", temperature=0.3, max_tokens=30)
    print("OUTPUT:", res.choices[0].message.content)
    print("REGEX:", re.findall(r'\d+', res.choices[0].message.content))
except Exception as e:
    print("ERROR:", e)
