from flask import Flask, request, jsonify
import json
import base64
import hmac
import hashlib
import sqlite3
import database

app = Flask(__name__)
database.create_user_table()

# 模拟的用户数据库
users = {}

# 生成JWT的函数
def create_jwt(username):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": username, "password": database.get_password(username)}
    secret = 'webservice-group-18'

    # 编码头部
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    # 编码载荷
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    # 生成签名
    signature = hmac.new(secret.encode(), f"{header_encoded}.{payload_encoded}".encode(), hashlib.sha256).digest()
    signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip('=')

    return f"{header_encoded}.{payload_encoded}.{signature_encoded}"

# 用户注册路由
@app.route('/users', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if database.is_existing_user(username):
        return jsonify({'detail':'duplicate'}), 409
    # users[username] = {'password': password}
    database.register_user(username, password)
    return jsonify(), 201

# 更新用户密码路由
@app.route('/users', methods=['PUT'])
def update_password():
    data = request.json
    username = data.get('username')
    old_password = data.get('password')
    new_password = data.get('new_password')
    if not database.is_existing_user(username):
        return jsonify({'detail':'forbidden'}), 403
    if database.is_existing_user(username):
        if database.verify_user(username, old_password):
            database.update_password(username, new_password)
            return jsonify(), 200
    return jsonify({'detail':'forbidden'}), 403

# 用户登录路由
@app.route('/users/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if database.verify_user(username, password):
        token = create_jwt(username)
        return jsonify({'token': token}), 200
    return jsonify({'detail':'forbidden'}), 403

# 运行Flask应用
if __name__ == '__main__':
    app.run(debug=True, port=5001)
