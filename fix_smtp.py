with open('main.py', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# In process_vip_loop
old_smtp = '''                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(req_email, req_pw)'''
new_smtp = '''                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.login(req_email, req_pw)'''
c = c.replace(old_smtp, new_smtp)

# In scan_inbox_and_reply (just in case)
old_smtp2 = '''                smtp = smtplib.SMTP('smtp.gmail.com', 587)
                smtp.starttls()
                smtp.login(email_addr, app_password)'''
new_smtp2 = '''                smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp.login(email_addr, app_password)'''
c = c.replace(old_smtp2, new_smtp2)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(c)
print('Fixed SMTP to use SSL')
