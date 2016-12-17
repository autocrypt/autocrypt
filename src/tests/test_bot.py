
from inbome.bot import generate_reply, send_reply

def test_generate_reply(datadir, gpg, smtpserver):
    with datadir.open("rsa2048-simple.eml") as fp:
        reply_msg = generate_reply(gpg, fp)
    assert reply_msg["To"] == "Alice <alice@testsuite.autocrypt.org>"
    assert reply_msg["From"] == "bot@autocrypt.org"
    assert reply_msg["INBOME"]

    host, port = smtpserver.addr

    send_reply(host, port, reply_msg)

    assert len(smtpserver.outbox) == 1



