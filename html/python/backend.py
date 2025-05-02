from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from wikidataConnection import get_country_info
from handleUsers import create_user
from DatabaseConnector import execute_query

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Javascript is able to interact with this function
@app.route('/api/country')
def country_info():
    country_name = request.args.get('name')
    if not country_name:
        return jsonify({'error': 'Missing parameters'}), 400
    result = get_country_info(country_name, 'population')
    return jsonify(result)

@app.route('/createUser')
def handle_create_user():
    username = request.args.get('name')
    if not username:
        return jsonify({'error': 'Missing parameters'}), 400
    create_user(username)
    return jsonify({'message': 'User created successfully'})


if __name__ == '__main__':
    app.run(debug=True)

