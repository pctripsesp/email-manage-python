# BASED ON:
# https://stackoverflow.com/questions/3362600/how-to-send-email-attachments

'''
HOW USE:
1. CHANGE to_email VARIABLE
2. CREATE config.ini FILE WITH YOUR EMAIL CREDENTIALS
3. CHANGE SUBJECT AND CONTENT OF EMAIL AS YOU NEED
4. CHANGE files VARIABLE WITH FILES PATH
5. CHANGE server VARIABLE WITH OTHER SMTP SERVER IF NOT GMAIL
6. python3 send_email_files.py
'''

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

# CONFIG.INI LOGIN
import configparser

# CONFIGPARSER
config = configparser.ConfigParser()
config.read('config.ini')
from_email = config['mail']['email']
password = config['mail']['password']

to_email = "TO_EMAIL@EXAMPLE.COM"

# MENSAJE
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = "MY SUBJECT"

contenido = "THIS IS THE CONTENT OF EMAIL"
msg.attach(MIMEText(contenido))

files = ['/home/USER/FILE1.pdf', '/home/USER/FILE2.pdf']
## ATTACH FILE
for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

# SMTP SERVER.
server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
server.login(from_email, password)
server.sendmail(from_email, to_email, msg.as_string())
server.close()

print("successfully sent email to %s:" % (msg['To']))
