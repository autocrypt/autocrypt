
from autocrypt.bot import generate_reply, send_reply

def test_generate_reply(datadir, bingpg, smtpserver):
    with datadir.open("rsa2048-simple-to-bot.eml") as fp:
        reply_msg = generate_reply(bingpg, fp)
    assert reply_msg["To"] == "Alice <alice@testsuite.autocrypt.org>"
    assert reply_msg["From"] == "bot@autocrypt.org"
    assert reply_msg["Autocrypt"]

    host, port = smtpserver.addr[:2]

    send_reply(host, port, reply_msg)

    assert len(smtpserver.outbox) == 1



