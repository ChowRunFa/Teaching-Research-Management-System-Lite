# -*- coding: utf-8 -*-
# @Time    : 2022/6/26 20:07
# @Author  : ChowRunFa
# @File    : app.py
# @Software: PyCharm
from flask import Flask, request
from flask_docs import ApiDoc

from gevent import pywsgi
from models import *
from server import MySQLConfig
from flask_cors import CORS

from api_create import api_create
from api_read import api_read
from api_update import api_update
from api_delete import api_delete
from utils import filter_props, generate_token, is_dict_valid, certify_token

app = Flask(__name__)
ApiDoc(
    app,
    title="Sample App",
    version="1.0.0",
    description="A simple app API",
)
app.config.from_object(MySQLConfig)
with app.app_context():
    db.init_app(app)
    db.create_all()

app.register_blueprint(api_create, url_prefix="")
app.register_blueprint(api_read, url_prefix="")
app.register_blueprint(api_update, url_prefix="")
app.register_blueprint(api_delete, url_prefix="")

cors = CORS(app, resources={r"/*": {"origins": "*"}}) # 注册CORS, "/*" 允许访问所有api


from functools import wraps
from flask import request, jsonify

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'code': 401, 'msg': '无效的 token'}), 401
        user_id = certify_token(token)
        if not user_id:
            return jsonify({'code': 401, 'msg': '无效的 token'}), 401
        return func(user_id=user_id, *args, **kwargs)
    return wrapper

@app.route('/api/login', methods=['POST'])
# 用户登录功能
def login():
    # 获取请求体中的数据
    data = request.get_json()
    print("data::",data)
    if not is_dict_valid(data):
        return result(400, 'error: 用户名或密码不完整！')
    workno = data['workno']
    name = data['name']
    # 根据工号从数据库中查询用户信息
    teacher = Teacher.query.get(workno)
    if not teacher:
        return result(400, 'error: 用户名不存在！')
    teacher_dict = filter_props(teacher)
    trueName = teacher.name
    # 验证用户名和密码是否正确
    if teacher and str(name) == str(trueName) :
        # 生成 token，并将用户信息和 token 返回给客户端
        token = generate_token(str(workno))
        return result(200, 'success', {'user': teacher_dict, 'token': token})
    else:
        return result(400, 'error: 密码错误！')
if __name__ == "__main__":
    # app.run(debug=True)
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    app.debug = True
    server.serve_forever()


