## BASED ON:
# https://codereview.stackexchange.com/questions/190035/python-use-imap-lib-to-download-attachments-and-email-details
## SOME RFC OPTIONS
# https://tools.ietf.org/html/rfc2060.html#page-38

'''
HOW USE
---------
1. CHANGE searchQuery VARIABLE AS YOU NEED
2. CHANGE filePath VARIABLE
3. CREATE A config.ini FILE WITH USERNAME AND PASS
4. MODIFY server VARIABLE WITH YOUR SERVER imap.example.com (HERE USING GMAIL)
5. ENJOY python3 save_email_attached.py
'''

import imaplib
import email.header
import os

import configparser

# CONFIGPARSER
config = configparser.ConfigParser()
config.read('config.ini')
EMAIL_ACCOUNT = config['mail']['email']
PASSWORD = config['mail']['password']
EMAIL_FOLDER = "INBOX"

# Connect to the server
server = imaplib.IMAP4_SSL('imap.gmail.com')

# Login to our account
server.login(EMAIL_ACCOUNT, PASSWORD)

server.select()

## DEFINE YOUR OWN SEARCH QUERY BASED ON RFC OPTIONS
'''
FROM, NOT FROM, SUBJECT, SINCE, UNSEEN, ALL...
date format --> SINCE 1-Oct-2018 ("Jan"/"Feb"/"Mar"/"Apr"/"May"/"Jun"/"Jul"/"Aug"/"Sep"/"Oct"/"Nov"/"Dec")
'''
searchQuery = 'FROM somebody@example.com SUBJECT hello UNSEEN'

result, data = server.uid('search', None, searchQuery)

ids = data[0]
# list of uids
id_list = ids.split()

i = len(id_list)
for x in range(i):
    latest_email_uid = id_list[x]

    # fetch the email body (RFC822) for the given ID
    result, email_data = server.uid('fetch', latest_email_uid, '(RFC822)')

    raw_email = email_data[0][1]

    # converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # downloading attachments
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        print("FILENAME:", fileName)

        if bool(fileName):
            ## CHANGE PATH HERE!!
            filePath = os.path.join('/home/', fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()


server.close()
server.logout()
