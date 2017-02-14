from __future__ import unicode_literals
import email.parser
import logging
import base64

def make_header(emailadr, keydata):
    assert keydata
    key = base64.b64encode(keydata)
    if isinstance(key, bytes):
        key = key.decode("ascii")
    l = ["to=" + emailadr, "key=" + key]
    return "Autocrypt: " + "; ".join(l)


def parse_message(fp):
    return email.parser.Parser().parse(fp)


def parse_message_from_string(string):
    return email.parser.Parser().parsestr(string)


def parse_autocrypt_header_from_string(string):
    msg = email.parser.Parser().parsestr(string)
    return extract_autocrypt_header(msg)


def extract_autocrypt_header(msg):
    autocrypt_headers = msg.get_all("Autocrypt")
    all_results = []
    if autocrypt_headers == None:
        logging.warn("found no Autocrypt header")
        return {}
    for inb in autocrypt_headers:
        res = parse_autocrypt_headervalue(inb)
        if res:
            all_results.append(res)
    if len(all_results) == 1:
        return all_results[0]
    if len(all_results) > 1:
        logging.warn("found more than one Autocrypt header, ignoring all")
    return {}


def parse_autocrypt_headervalue(value):
    parts = value.split(";")
    result_dict = {}
    for x in parts:
        kv = x.split("=", 1)
        name = kv[0].strip()
        value = kv[1].strip()
        if name == "to":
            result_dict["to"] = value
        elif name == "key":
            keydata_base64 = "".join(value.split())
            keydata = base64.b64decode(keydata_base64)
            result_dict["key"] = keydata
        elif name == "type":
            result_dict["type"] = value
        elif name == "prefer-encrypted":
            result_dict["prefer-encrypted"] = value
        elif name[0] == "_":
            logging.warn("found non-critical %r header attribute, ignoring it", name)
        else:
            logging.warn("found unknown critical attribute, ignoring header")
            return {}
    if "key" not in result_dict:
        logging.warn("found no key, ignoring header")
    elif "to" not in result_dict:
        logging.warn("found no to e-mail address, ignoring header")
    elif "type" in result_dict and result_dict["type"] != "p":
        logging.warn("found type %r, but we only support 'p'", result_dict["type"])
    elif "prefer-encrypted" in result_dict and result_dict["prefer-encrypted"] not in ["yes", "no"]:
        logging.warn("found prefer-encrypted %r, but we only support yes or no",
                     result_dict["prefer-encrypted"])
    else:
        return result_dict

