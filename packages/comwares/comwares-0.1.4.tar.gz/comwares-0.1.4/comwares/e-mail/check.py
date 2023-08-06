import os
import imaplib
import email
from email.header import decode_header


def get_imap_conn(email: str, password: str, mailbox: str = "INBOX",
                  imap_host: str = "imap.exmail.qq.com", imap_port: int = 993):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(imap_host, imap_port)
    mail.login(email, password)
    # Select the mailbox (default is "INBOX")
    mail.select(mailbox)
    return mail


def extract_email(msg_data, attachments_dir: str = '/Users/kevinzhu/tmp') -> dict:
    info = dict()
    info['attachments'] = []
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

            charset = decode_header(msg["Subject"])[0][1]
            charset = 'utf-8' if not charset else charset

            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode(charset)
            info['subject'] = subject
            info['from'] = msg.get("From")
            info['date'] = msg.get("Date")

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain":
                        body = part.get_payload(decode=True)
                        info['body'] = body

                    elif content_type == "text/html":
                        body = part.get_payload(decode=True)
                        info['body'] = body

                    elif content_type == "multipart/alternative":
                        body = part.get_payload(decode=True)
                        info['body'] = body

                    elif "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            charset = decode_header(filename)[0][1]
                            filename = decode_header(filename)[0][0]
                            if isinstance(filename, bytes):
                                filename = filename.decode(charset)

                            if not os.path.exists(attachments_dir):
                                os.makedirs(attachments_dir)
                            filepath = os.path.join(attachments_dir, filename)
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            info['attachments'].append(filepath)

                    else:
                        print(subject)
                        print(content_type)
                        print()

            else:
                body = msg.get_payload(decode=True)
                info['body'] = body

    return info


def get_messages(mailbox: imaplib.IMAP4_SSL, keyword: str = 'ALL') -> list:
    status, messages = mailbox.search(None, keyword)
    messages = messages[0].split(b' ')
    processed = []
    for msg_num in messages:
        _, msg_data = mailbox.fetch(msg_num, "(RFC822)")
        mail_info = extract_email(msg_data)
        processed.append(mail_info)
    mailbox.logout()
    return processed


if __name__ == "__main__":
    email_address = "zhujianfeng@x-port.com.cn"
    password = "KBvugJpgzuGaPs6Z"
    conn = get_imap_conn(email_address, password, mailbox='&UXZO1mWHTvZZOQ-/invoice')
    mails = get_messages(mailbox=conn, keyword='(FROM "niuguozun")')

