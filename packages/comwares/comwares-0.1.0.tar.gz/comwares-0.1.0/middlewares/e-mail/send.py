import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject, body, to_email, from_email, username, password, smtp_server, smtp_port):

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:  # Secure the connection
            server.login(username, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending e-mail: {e}")


if __name__ == "__main__":

    subject = "Test e-mail"
    body = "This is a test e-mail sent using Python."
    to_email = "kevin.zhu.work@gmail.com"
    from_email = "zhujianfeng@x-port.com.cn"
    username = from_email
    password = "KBvugJpgzuGaPs6Z"
    smtp_host = 'smtp.exmail.qq.com'
    smtp_port = 465
    send_email(subject, body, to_email, from_email, username, password, smtp_host, smtp_port)
