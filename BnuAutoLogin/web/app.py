import os
from datetime import timedelta

from BnuAutoLogin.web.blueprintes import lg
from flask import Flask,redirect,url_for

app = Flask(__name__)
app.register_blueprint(lg.lg)

# 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['SECRET_KEY'] = os.urandom(24)

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
    minutes=30)  # 设置session的保存时间。

app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return redirect(url_for("lg.login"))


def run_server():
    app.run(host='0.0.0.0', port=2020, debug=True)


if __name__ == "__main__":
    run_server()
