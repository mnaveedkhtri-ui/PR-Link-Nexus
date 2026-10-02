with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Right after dynamic_niche is extracted, let's log it to DB
syslog_code = '''
    dynamic_niche = extract_niche_with_ai(client, scraped_text)
    log_pitch_to_db("SYSTEM LOG", "AI Niche", f"Extracted Niche: {dynamic_niche}", "LOG", "LOG")
'''
c = c.replace('dynamic_niche = extract_niche_with_ai(client, scraped_text)', syslog_code)

# After extracting queries
syslog_code2 = '''
    live_feeds, haro_logs = fetch_live_queries_from_haro(req_email, req_pw)
    log_pitch_to_db("SYSTEM LOG", "IMAP Scanner", f"Found {len(live_feeds)} PR queries in inbox", "LOG", "LOG")
'''
c = c.replace('live_feeds, haro_logs = fetch_live_queries_from_haro(req_email, req_pw)', syslog_code2)

# After AI filter
syslog_code3 = '''
        log_pitch_to_db("SYSTEM LOG", "AI Filter", f"AI selected {len(selected_indices)} matching queries to pitch", "LOG", "LOG")
'''
c = c.replace('logs.append(f"> [*] BATCH COMPLETE. AI selected {len(selected_indices)} creative matching queries!")', 'logs.append(f"> [*] BATCH COMPLETE. AI selected {len(selected_indices)} creative matching queries!")\n' + syslog_code3)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Added syslogs to DB')
