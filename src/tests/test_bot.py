
from autocrypt.bot import generate_reply, send_reply


def test_botkey_load_and_sign(bingpg, datadir):
    keydata = datadir.read_bytes("testbot.secretkey")
    keyid = bingpg.import_keydata(keydata)
    sigdata = bingpg.sign(data=b"123", keyid=keyid)
    bingpg.verify(data=b'123', signature=sigdata)


def test_generate_reply(datadir, bingpg, smtpserver):
    with datadir.open("rsa2048-simple-to-bot.eml") as fp:
        reply_msg = generate_reply(bingpg, fp)
    assert reply_msg["To"] == "Alice <alice@testsuite.autocrypt.org>"
    assert reply_msg["From"] == "bot@autocrypt.org"
    assert reply_msg["Autocrypt"]

    host, port = smtpserver.addr[:2]

    send_reply(host, port, reply_msg)

    assert len(smtpserver.outbox) == 1



