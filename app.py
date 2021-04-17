# -*- coding: utf-8 -*-

import json
import os
import sys
import time
import traceback
from server import update_codes as git_uc

from flask import Flask, redirect, url_for, request, session, render_template, send_from_directory, Response

from scripts.functions import formate_mybatis as fm
from scripts.functions import get_sql_table as gst
from scripts.functions import quote_str_list as qs
from scripts.feedback import ffb_opt
from scripts.hash_text import shb_opt

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only
app.register_blueprint(ffb_opt)
app.register_blueprint(shb_opt)


# Heroku
# from flask_heroku import Heroku
# heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('sql_tables.html')


@app.route('/restart', methods=['GET'])
def restart():
    lines = git_uc()
    # py = sys.executable
    # os.execl(py, py, *sys.argv)
    return '\n'.join(lines)


@app.route('/sql-tables', methods=['GET', 'POST'])
def sql_tables():
    return render_template('sql_tables.html')


@app.route('/mybatis-log-format', methods=['GET'])
def mybatis_log_format():
    return render_template('mybatis_log_format.html')


@app.route('/text-formator', methods=['GET', 'POST'])
def text_formatter():
    return render_template('text_formator.html')


@app.route('/file-feed-back', methods=['GET'])
def file_feed_back():
    return render_template('file_feed_back.html')


@app.route('/text-hash', methods=['GET'])
def text_hash_path():
    return render_template('text_hash.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


# -----------------------------------------------------------

@app.route('/do-get-tables', methods=['POST'])
def do_get_tables():
    sql = request.form['data']
    tables = gst.extract_table_name_from_sql(sql)
    return json.dumps('\n'.join(tables))


@app.route('/do-quote-strs', methods=['POST'])
def do_quote_str():
    data = request.form
    pre = '"' if data['pre'] is None else data['pre']
    after = '"' if data['after'] is None else data['after']
    ls = qs.quote(data['txt'], data['df'], pre, after)
    return json.dumps(ls, ensure_ascii=False)


@app.route('/do-format-msl', methods=['POST'])
def do_format_sql():
    data = request.form['data']
    try:
        res = fm.do_format(data)
    except Exception as ex:
        traceback.print_exc()
        return "处理发生异常:" + str(ex)
    return json.dumps(res, ensure_ascii=False)


# ======== Main ============================================================== #
if __name__ == "__main__":
    print(sys.path[0])
    _port = 80
    try:
        _port = int(sys.argv[1]) if int(sys.argv[1]) > 1024 else 80
    except (ValueError, IndexError):
        pass
    print("服务启动@", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=_port)
