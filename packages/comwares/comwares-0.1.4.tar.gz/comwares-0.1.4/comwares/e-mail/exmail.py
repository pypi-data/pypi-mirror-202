import imaplib
import email
from email.parser import BytesParser
from email.utils import parseaddr


def get_imap_conn(email: str, token: str, host: str = 'imap.exmail.qq.com'):
    host = 'imap.exmail.qq.com'
    conn = imaplib.IMAP4(host)
    conn.login(email, token)
    return conn


def get_email_list(conn: imaplib.IMAP4, mail_dir: str = 'INBOX'):
    conn.select(mail_dir)
    status, data = conn.search(None, 'ALL')
    email_list = list(reversed(data[0].split()))
    return email_list


def decode_str(s):
    try:
        subject = email.header.decode_header(s)
    except:
        # print('Header decode error')
        return None
    sub_bytes = subject[0][0]
    sub_charset = subject[0][1]
    if not sub_charset:
        subject = sub_bytes
    elif 'unknown-8bit' == sub_charset:
        subject = str(sub_bytes, 'utf8')
    else:
        subject = str(sub_bytes, sub_charset)
    return subject


def get_email(conn: imaplib.IMAP4, num: str):
    typ, content = conn.fetch(num, '(RFC822)')
    msg = BytesParser().parsebytes(content[0][1])
    sub = msg.get('Subject')
    for part in msg.walk():
        filename = part.get_filename()
        filename = decode_str(filename)
        if filename:
            print('+++++++++++++++++++')
            print(filename)
            data = part.get_payload(decode=True)
            try:
                f = open(filename, 'wb')
                f.write(data)
                f.close()
                print(f'Saved file: {filename}')
            except Exception as e:
                print(e)
    return decode_str(sub)


