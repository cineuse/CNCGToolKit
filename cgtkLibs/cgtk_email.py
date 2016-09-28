# coding=utf8

from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib
from cgtk_config import studio_config


def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def send_mail(to_addr, subject_string, body, image=None):
    email_cfg = studio_config.get('email')
    from_addr = email_cfg['from']
    password = email_cfg['password']
    smtp_server = email_cfg['smtp_server']
    body_string = body
    msg_root = MIMEMultipart('related')
    msg_root['From'] = format_addr('cgtk-%s<%s>' % (email_cfg["name"], from_addr))
    msg_root['To'] = format_addr('user<%s>' % to_addr)
    msg_root['Subject'] = Header(subject_string, 'utf-8').encode()
    if image is not None:
        msg_text = MIMEText(body_string + '<br><img src="cid:image1">', 'html')
        msg_root.attach(msg_text)
        fp = open(image, 'rb')
        msg_image = MIMEImage(fp.read())
        fp.close()
        msg_image.add_header('Content-ID', '<image1>')
        msg_root.attach(msg_image)
    else:
        msg_text = MIMEText(body_string, 'html')
        msg_root.attach(msg_text)

    smtp_port = int(email_cfg['port'])
    if email_cfg['ssl'] == 'yes':
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    else:
        server = smtplib.SMTP(smtp_server, smtp_port)
    # server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg_root.as_string())
    server.quit()


if __name__ == "__main__":
    send_mail("guoliangxu1987@qq.com", "CGTK Test", "Hello, this is a test", image=None)
