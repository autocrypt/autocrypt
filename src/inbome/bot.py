"""

simple bot functionality to work answering for bot@autocrypt.org

"""

import os, sys
import logging
from inbome.parse import extract_inbome_header, parse_message
from inbome.gpg import GPG
import email.parser
from email.mime.text import MIMEText
import smtplib


MY_ADR = "bot@autocrypt.org"
KEY_ID = "9305817E"
ikey = """\
 mQENBFhVGUgBCACtkVZIUlZIvGmjPVYnOfI2UlXS5kapT9bgfTCgq3JcFbwdZJH3ka3Xoq+Bgmzc
 dKSwY9Y4N9TqfDYkacuagRvziYQH8rTSKKeRMmdfC/GJgakAZbvcwHqbT3P3QDCi6l3RIyvoRv6U
 Si2HrS9OR2s4AoToHtTbF3C13fcRs71ffxBfu6IYWKxZyjGqM/S0hUTSLbO0GuktCuw2TlJxOo39
 +2dlLMGMMXp0Vz9IQ1Ul7pul3TG2QOaDONBjnBopBQ4WLwQf7NVaKRLBx7F21mwCgoJmNmgs/iLv
 rIi509G8PXzYQOcTTLG7AtE9+prcEWh3XhaUEXYjpR7lfhLsE8bxABEBAAG0IWF1dG9jcnlwdCBi
 b3QgPGJvdEBhdXRvY3J5cHQub3JnPokBOAQTAQIAIgUCWFUZSAIbAwYLCQgHAwIGFQgCCQoLBBYC
 AwECHgECF4AACgkQv17Dg5MFgX4OFggAjcVSQenriYU+uE/PEVuLojF8CdqwA1vBeiUpK9fCYtHd
 FW9g9diebhtTPUG4eU3Z7A0OiRbV7OsuQDlttHlgoQIRMiH+dAjcQxDxObLLcngoXi0XZRgIuZ6z
 WhSNgPQxpKvz8IcDHgoL8hdC5YXcvZ0B3rOjQkF+3qFmU9zDkAWYMkxt9Gt1fW9wS8JwGKCZBQH3
 pGwtznzHBI6rM0LnpqEmA1WgvUWWIFdRXOA1J4HnCa5CeBV09iXV69qU/4pvtuh5V8eIqGsxHNky
 Pg+FyeafMLjNJNvGSZzCkG6ec4R3s6rtsmLMAW61detDxrNCYk4oNLnTmWqEdowpOpwJhLkBDQRY
 VRlIAQgA9sRsP3K4gZEcIbkgymPh4Mw5t2RmpCVMx5yNriA4IUhUOjcHq1ZNDJ1ZtN25eUvyE2iD
 QY9xE9QkxeNODpQC7qAWjsi6nPQu+7ALmKSZKHZhUUsDWX0Rjx+VN1cMgOcMBIIA5hWBBJL0jJOs
 3zIHYUHPHKgWQH34FU7/8tm0R5uvn6LYQhGzKhVXXkkI3JrhE+8G3HXKj4k8E1n7Ja9w4o5LXvCF
 7L5lnw1CiuGpaKmzjk1bKhj1d/Wr3G0z510WoWC6m2mCm/l7ncXWYMTd/VUoCzdKXpBR9SEcFhFi
 8HO1fGvdxmt6A6G8rLb9UYDO45+oMIpl44KtkHj3t4BLcQARAQABiQEfBBgBAgAJBQJYVRlIAhsM
 AAoJEL9ew4OTBYF+a4IIAI3VUou7Ml6NejlQ7A+eYFEcSIUYkkDPUJc4a4hc2Uvy4Spn6wDV7KqN
 iSae0//8q8jm8LFCAuFq2Gt0hd8YOVD+g6x6+Mim2RJPeQM3EYTeYJcKV3so/TGAJY6xQ7kTYT5n
 ofkXOYG6HE2IGN7sRy1gKhIEVss0T9RoaVyKBCv9PSAcXq+NWRVvvoUhvP17/D3otnnX9fcYmTHx
 Y7WcrgeM31V6ZixkBeU1XoFohMcm4NdhB/zzpqxttc1LUamlXMrle/7QaY3pRRki+n3u4IFFO3bW
 jsvC6lHj97g8jmrFQpdFBl8VgHeIJfSl3b5d8K8JnA1Sfo4OxD5/zR3RPM0=
"""
INBOME_HEADER = "to=bot@autocrypt.org; key=\n" + ikey

def generate_reply(gpg, fp):
    msg = parse_message(fp)
    from_header = msg.get_all("from")
    subject = msg.get_all("subject")
    inbome_header = extract_inbome_header(msg)

    logging.info("got mail: %s", msg.as_string())

    reply_msg = MIMEText('''Autoresponse''')
    reply_msg['Subject'] = "Re: " + msg["Subject"]
    reply_msg['From'] = MY_ADR
    reply_msg['To'] = msg["From"]
    reply_msg["INBOME"] = INBOME_HEADER

    return reply_msg

def send_reply(host, port, msg):
    smtp = smtplib.SMTP(host, port)
    logging.info("sending reply: %s", msg.as_string())
    return smtp.sendmail(MY_ADR, msg["To"], msg.as_string())

def main():
    gpg = GPG(os.path.expanduser("~/keyring"))
    reply_msg = generate_reply(gpg, sys.stdin)
    return send_reply(reply_msg)

if __name__ == "__main__":
    main()
