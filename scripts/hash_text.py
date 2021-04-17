import json
import os
import hashlib
import base64

from flask import Flask, Blueprint, request

app = Flask(__name__)
app.secret_key = os.urandom(12)
shb_opt = Blueprint("hashtext", __name__)

SALT = "1B2M2Y8AsgTpgAmY7PhCfg=="


@shb_opt.route('/do-text-hash', methods=['POST'])
def deal_hash_base64():
    data = request.form
    text = str(data['txt']).split("\n")
    texts = []
    for line in text:
        texts.append(do_hash_base64(line))
    return json.dumps(texts, ensure_ascii=False)


def do_hash_base64(src):
    src = src + SALT
    sha = hashlib.sha256(src.encode('utf-8')).digest()
    b64 = base64.encodebytes(sha)
    b64_str = b64.decode("utf-8")
    return b64_str


if __name__ == '__main__':
    r = do_hash_base64("赵磊")
    print(r)
