import json
import os
import sys
import time

from flask import request, Response, Flask, Blueprint
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = os.urandom(12)
ffb_opt = Blueprint("feedfileback", __name__)


@ffb_opt.route('/do-feed-back', methods=['POST'])
def do_feed_back():
    f = request.files['file']
    exists = os.path.exists(get_store_path())
    # 判断结果
    if not exists:
        os.makedirs(get_store_path())
    s = time.strftime("%Y%m%d%H%M%S", time.localtime())
    f.save(get_store_path() + "/" + s + "-" + f.filename)
    return "Ok"


@ffb_opt.route('/list-feed-file', methods=['GET'])
def list_feed_file():
    res = []
    for files in os.walk(get_store_path()):
        for file in files[2]:
            res.append(file)
    return json.dumps(res, ensure_ascii=False)


@ffb_opt.route("/download-feed-file", methods=['GET'])
def download_feed_file():
    filename = request.args.get('fn')

    # return send_from_directory(r"" + get_store_path(), filename=filename, as_attachment=True)
    def send_file():
        store_path = os.path.join(get_store_path(), filename)
        with open(store_path, 'rb') as targetfile:
            while 1:
                data = targetfile.read(1 * 1024 * 1024)  # 每次读取1MB (可用限速)
                if not data:
                    break
                yield data

    response = Response(send_file(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename=%s' % quote(filename.encode('utf-8'))
    return response


@ffb_opt.route("/delete-feed-file", methods=['GET'])
def delete_feed_file():
    filename = request.args.get('fn')
    store_path = os.path.join(get_store_path(), filename)
    os.remove(store_path)
    return "Ok"

def get_store_path():
    return sys.path[0] + "/files"
