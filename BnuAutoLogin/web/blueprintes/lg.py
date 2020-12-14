from flask import Blueprint, render_template,redirect,request

lg = Blueprint('lg', __name__, url_prefix="/lg")

# 登录
@lg.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('lg_login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        print(username,password)
        try:
            # 待处理登录
            pass
        except Exception as e:
            return render_template('lg_login.html', error="用户名或密码错误")
        return redirect(url_for('lg.success'))

# 登录成功
@lg.route('/success/', methods=['GET', 'POST'])
def success():
    pass