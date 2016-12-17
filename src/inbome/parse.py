
import email.parser
import logging
import base64


def parse_inbome_header(fp):
    p = email.parser.Parser()
    msg = p.parse(fp)
    inbome_headers = msg.get_all("INBOME")
    all_results = []
    for inb in inbome_headers:
        res = parse_inbome_headervalue(inb)
        if res:
            all_results.append(res)
    if len(all_results) == 1:
        return all_results[0]
    if len(all_results) > 1:
        logging.warn("found more than one INBOME header, ignoring all")
    return {}


def parse_inbome_headervalue(value):
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
        else:
            logging.warn("found %r header value, ignoring it", name)
    if "key" not in result_dict:
        logging.warn("found no key, ignoring header")
    elif "to" not in result_dict:
        logging.warn("found no to user id, ignoring header")
    else:
        return result_dict

