# -*- coding: utf-8 -*-

import json
import os
import time

from flask import Flask, redirect, url_for, request, session, render_template

from scripts.functions import get_sql_table as gst
from scripts.functions import quote_str_list as qs
from scripts.functions import formate_mybatis as fm

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only


# Heroku
# from flask_heroku import Heroku
# heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('sql_tables.html')


@app.route('/sql-tables', methods=['GET', 'POST'])
def sqlTables():
    return render_template('sql_tables.html')

@app.route('/mybatis-log-format', methods=['GET'])
def mybatisLogFormat():
    return render_template('mybatis_log_format.html')

@app.route('/text-formator', methods=['GET', 'POST'])
def text_formator():
    return render_template('text_formator.html')


@app.route('/tables', methods=['GET', 'POST'])
def tables():
    return render_template('tables.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


@app.route('/do-get-tables', methods=['POST'])
def do_get_tables():
    sql = request.form['data']
    tables = gst.extract_table_name_from_sql(sql)
    return json.dumps('\n'.join(tables))


@app.route('/do-quote-strs', methods=['POST'])
def do_quote_str():
    data = json.loads(request.get_data(as_text=True))
    pre = '"' if data['pre'] is None else data['pre']
    after = '"' if data['after'] is None else data['after']
    ls = qs.quote(data['txt'], data['df'], pre, after)
    return json.dumps('\n'.join(ls))


@app.route('/do-format-msl', methods=['POST'])
def do_format_sql():
    data = request.form['data']
    try:
        res = fm.do_format(data)
    except Exception as ex:
        print("出现如下异常%s"%ex)
        return "处理发生异常..."
    return json.dumps('\n'.join(res))


# ======== Main ============================================================== #
if __name__ == "__main__":
    print("服务启动@", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
