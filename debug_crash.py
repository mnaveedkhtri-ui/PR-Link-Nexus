with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

debug_endpoint = '''@app.post("/api/debug-crash")
def debug_crash(req: VIPRequest):
    import traceback
    try:
        client = Groq(api_key=GROQ_API_KEY)
        req_email = req.sender_email or os.getenv("SENDER_EMAIL")
        req_pw = req.app_password or os.getenv("APP_PASSWORD")
        req_name = req.founder_name or os.getenv("FOUNDER_NAME")
        req_url = req.website_url or os.getenv("WEBSITE_URL")
        
        live_feeds, haro_logs = fetch_live_queries_from_haro(req_email, req_pw)
        if not live_feeds:
            return {"error": "No live feeds found"}
            
        item = live_feeds[0]
        dynamic_niche = "Test Niche"
        system_prompt = f"""
        You are {req_name}, a busy founder at {req_url}.
        Your expertise: {dynamic_niche}.
        You are emailing a journalist to provide a quick quote for their story.
        
        CRITICAL RULES FOR 100% HUMAN STYLE:
        1. Find a creative, unique angle connecting your expertise to their query.
        2. Write like a real, busy person. Extremely conversational and casual.
        3. Maximum 3 sentences total. Keep it punchy.
        4. USE LINE BREAKS (paragraphs) between sentences so it's easy to read.
        5. Start with "Hi {item['name']},".
        6. Sign off simply with:
        Best,
        {req_name}
        {req_url}
        """
        pitch_text = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Journalist Query: \\"{item['query']}\\"\\nWrite the email."}],
            model="qwen/qwen3.8-27b", temperature=0.7, max_tokens=250
        ).choices[0].message.content
        
        return {"success": True, "pitch": pitch_text}
    except Exception as e:
        return {"error": traceback.format_exc()}
'''

c = c.replace('if __name__ == "__main__":', debug_endpoint + '\nif __name__ == "__main__":')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Added debug crash endpoint')
