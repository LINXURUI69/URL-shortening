from flask import Flask, request, jsonify
import random
import re
import json
import base64
import hmac
import hashlib

import database

app = Flask(__name__)
url_mapping = {}
secret = 'webservice-group-18'

# Generate a short identifier for a new URL
def generate_short_id(length):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    chars_arr = list(chars)
    radix = len(chars)
    quotient = int(length)
    arr = []
    while quotient:
        mod = quotient % radix
        quotient = (quotient - mod) //radix
        arr.insert(0, chars_arr[mod])
    return ''.join(arr)

def jwt_extraction(token):
    t = token.split('.')
    header = decode_base64(t[0]).decode('utf-8')
    payload = decode_base64(t[1]).decode('utf-8')
    signature = decode_base64(t[2]).decode('utf-8')
    return header, payload, signature

def decode_base64(data):
    # 确保字符串长度是 4 的倍数
    padding = 4 - (len(data) % 4)
    data += "=" * padding
    return base64.urlsafe_b64decode(data)

def bytes_decode(data):
    data = base64.urlsafe_b64decode(data + "==")
    str = data.decode('utf-8')
    result = json.loads(str)
    return result

def verify_jwt_signature(jwt_token, secret_key):
    # 分割JWT，获取Header, Payload和Signature
    header, payload, signature = jwt_token.split('.')
    # 对Header和Payload进行base64解码
    decoded_header = base64.urlsafe_b64decode(header + '==')
    decoded_payload = base64.urlsafe_b64decode(payload + '==')
    # 重建用于签名的数据
    signing_input = header + '.' + payload
    # 使用HMAC和SHA256算法生成新的签名
    new_signature = hmac.new(
        key=secret_key.encode(),
        msg=signing_input.encode(),
        digestmod=hashlib.sha256
    ).digest()
    # 对新生成的签名进行base64编码
    new_signature_encoded = base64.urlsafe_b64encode(new_signature).rstrip(b'=')
    # 对原始签名进行解码
    decoded_signature = base64.urlsafe_b64decode(signature + '==')
    # 比较新旧签名
    return hmac.compare_digest(new_signature_encoded, decoded_signature)
# Generate a short identifier for a new URL
'''def generate_short_identifier():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    short_id = ''.join(random.choice(characters) for i in range(6))  # Generate a 6-character short ID
    return short_id'''

# Check URL validity using a regex expression
# pattern cited from https://medium.com/@dilarauluturhan/javascript-regex-regular-expressions-e4485ffe719c
def is_valid_url(url):
    pattern = r'^(https?|ftp):\/\/[^\s\/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None

def is_valid_jwt(token):
    if token is None:
        return False
    pattern = r'^[^.]+\.+[^.]+\.+[^.]+$'
    return re.match(pattern, token) is not None

def get_username(token):
    header, payload, signature = token.split('.')
    username = bytes_decode(payload).get('sub')
    return username

def is_username_match(token, url_id):
    return get_username(token) == url_mapping[url_id]['username']

def is_user_in_mapping(username):
    for key in url_mapping:
        if url_mapping[key]['username'] == username:
            return True
    return False

def del_urls_by_username(username):
    keys_to_delete = [key for key, value in url_mapping.items() if value.get('username') == username]
    for key in keys_to_delete:
        del url_mapping[key]
    return True

# Resolve a short identifier to a full URL
@app.route('/<string:url_id>', methods=['GET'])
def resolve_url(url_id):
    token = request.headers.get('Authorization')
    if is_valid_jwt(token) is False:
        return jsonify({'detail': 'forbidden'}), 403
    if url_id in url_mapping:
        if not is_username_match(token, url_id):
            return jsonify({'detail': 'forbidden'}), 403
        return jsonify({'value': url_mapping[url_id].get('value')}), 301
    else:
        return jsonify({'error': 'URL not found'}), 404

# Create a new URL mapping
@app.route('/', methods=['POST'])
def create_url_mapping():
    token = request.headers.get('Authorization')
    if is_valid_jwt(token) is False:
        return jsonify({'detail': 'forbidden'}), 403
    if database.is_existing_user(get_username(token)) is False:
        return jsonify({'detail': 'forbidden'}), 403
    raw_data = request.get_data()
    data = json.loads(raw_data)
    if 'value' in data and is_valid_url(data['value']):
        length = len(url_mapping) + 1
        short_id = generate_short_id(length)
        #short_id = generate_short_identifier()
        url_mapping[short_id] = {'value': data['value'], 'username': get_username(token)}
        return jsonify({'id': short_id}), 201
    else:
        return jsonify({'error': 'Invalid URL'}), 400

# Delete a URL mapping with url_id
@app.route('/<string:url_id>', methods=['DELETE'])
def delete_url_mapping(url_id):
    token = request.headers.get('Authorization')
    if is_valid_jwt(token) is False:
        return jsonify({'detail': 'forbidden'}), 403
    if not url_id in url_mapping:
        return jsonify({'error': 'URL not found'}), 404
    if url_id in url_mapping:
        if not is_username_match(token, url_id):
            return jsonify({'detail': 'forbidden'}), 403
        del url_mapping[url_id]
        return '', 204

# Delete all URL mappings
@app.route('/', methods=['DELETE'])
def delete_all_url_mappings():
    token = request.headers.get('Authorization')
    if is_valid_jwt(token) is False:
        return jsonify({'detail': 'forbidden'}), 403
    if database.is_existing_user(get_username(token)) is False:
        return jsonify({'detail': 'forbidden'}), 403
    del_urls_by_username(get_username(token))
    return '', 404

# Get all url mappings
@app.route('/', methods=['GET'])
def get_all_url_mappings():
    token = request.headers.get('Authorization')
    if is_valid_jwt(token) is False:
        return jsonify({'detail': 'forbidden'}), 403
    if is_user_in_mapping(get_username(token)) is False:
        return jsonify({'detail': 'forbidden'}), 403
    if len(url_mapping) == 0:
        return jsonify({'error': 'No URL mappings found'}), 404
    else:
        tmp_map = {}
        for url_id in url_mapping:
            if url_mapping[url_id]['username'] == get_username(token):
                tmp_map[url_id] = url_mapping[url_id]['value']
        return jsonify(tmp_map), 200

    
# Update a URL mapping
@app.route('/<string:url_id>', methods=['PUT']) 
def update_url_mapping(url_id):
    token = request.headers.get('Authorization')
    if is_valid_jwt(token) is False:
        return jsonify({'detail': 'forbidden'}), 403
    raw_data = request.get_data()
    data = json.loads(raw_data)
    if url_id in url_mapping:
        if is_username_match(token, url_id) is False:
            return jsonify({'detail': 'forbidden put'}), 403
        if 'url' in data and is_valid_url(data['url']):
            url_mapping[url_id]['value'] = data['url']
            return jsonify({'url': data['url'],'id': url_id}), 200
        else:
            return jsonify({'error': 'Invalid URL'}), 400
    else:
        return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
