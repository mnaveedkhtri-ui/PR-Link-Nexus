with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the exception logging to also write to the database
old_exc = '''                except Exception as e:
                    logs.append(f"> [*] SMTP ERROR: {e}")'''

new_exc = '''                except Exception as e:
                    logs.append(f"> [*] SMTP ERROR: {e}")
                    log_pitch_to_db("SYSTEM LOG", "Error in Pitch", str(e), "ERROR")
'''
c = c.replace(old_exc, new_exc)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Added error logging to DB')
