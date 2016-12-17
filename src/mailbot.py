import inbome

import email.parser
from email.mime.text import MIMEText
import smtplib

def handle_message():
    parser = email.parser.Parser()

    msg = p.parse(sys.stdin)
    from_header = msg.get_all("from")
    subject = msg.get_all("subject")
    inbome_header = parse_inbome_header(fp)
    #TODO: extract key
    reply(to_address, subject)
    return

def reply(to_address,subject):
    smtp_server = smtplib.SMTP('localhost')
    me = 'bot@autocrypt.org'
    msg = MIMEText('Autoresponse')
    msg['Subject'] = "Re:"+ subject
    msg['From'] = me
    msg['To'] = to_address
    
    # TODO: Add inbome header
    
    smtp_server.sendmail(me, to_address, msg.as_string())
    smtp_server.quit()


    return




def main():







