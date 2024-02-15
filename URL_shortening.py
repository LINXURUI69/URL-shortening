from flask import Flask, request, jsonify
import random
import re
import json

app = Flask(__name__)
url_mapping = {}

# Generate a short identifier for a new URL
def generate_short_id(length):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    chars_arr = list(chars)
    radix = len(chars);
    quotient = int(length);
    arr = []
    while quotient:
        mod = quotient % radix
        quotient = (quotient - mod) //radix
        arr.insert(0, chars_arr[mod])
    return ''.join(arr)

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

# Resolve a short identifier to a full URL
@app.route('/<string:url_id>', methods=['GET'])
def resolve_url(url_id):
    if url_id in url_mapping:
        return jsonify({'value': url_mapping[url_id]}), 301
    else:
        return jsonify({'error': 'URL not found'}), 404

# Create a new URL mapping
@app.route('/', methods=['POST'])
def create_url_mapping():
    raw_data = request.get_data()
    data = json.loads(raw_data)
    if 'value' in data and is_valid_url(data['value']):
        length = len(url_mapping) + 1
        short_id = generate_short_id(length)
        #short_id = generate_short_identifier()
        url_mapping[short_id] = data['value']
        return jsonify({'id': short_id}), 201
    else:
        return jsonify({'error': 'Invalid URL'}), 400

# Delete a URL mapping with url_id
@app.route('/<string:url_id>', methods=['DELETE'])
def delete_url_mapping(url_id):
    if url_id in url_mapping:
        del url_mapping[url_id]
        return '', 204
    else:
        return jsonify({'error': 'URL not found'}), 404

# Delete all URL mappings
@app.route('/', methods=['DELETE'])
def delete_all_url_mappings():
    url_mapping.clear()
    return '', 404

# Get all url mappings
@app.route('/', methods=['GET'])
def get_all_url_mappings():
    if len(url_mapping) == 0:
        return jsonify({'error': 'No URL mappings found'}), 404
    else:
        return jsonify(url_mapping), 200
    
# Update a URL mapping
@app.route('/<string:url_id>', methods=['PUT']) 
def update_url_mapping(url_id):
    raw_data = request.get_data()
    data = json.loads(raw_data)
    if url_id in url_mapping:
        if 'url' in data and is_valid_url(data['url']):
            url_mapping[url_id] = data['url']
            return jsonify({'url': data['url'],'id': url_id}), 200
        else:
            return jsonify({'error': 'Invalid URL'}), 400
    else:
        return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
