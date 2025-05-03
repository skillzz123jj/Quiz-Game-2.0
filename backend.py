from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS
import requests
from wikidataConnection import get_country_info
from handleUsers import create_user, login_user
from DatabaseConnector import execute_query

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'60b676f51c4358745dae296b0e13f16261076c508030a35a3d3c58ebb0717fc8'

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
    session["username"] = username
    return jsonify({'message': 'User created successfully'})

@app.route('/start-menu')
def start_menu():
    return render_template("start-menu.html")

@app.route('/main-menu')
def main_menu():
    # TODO: tell the template if the user has a save file.
    #  If the save file doesn't exist, the template should
    #  disable the "Load game" button
    return render_template(
        "main-menu.html",
        username=session.get("username")
    )

@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        username = request.form["username"]
        if not username:
            # TODO: show an error to the user
            return render_template("create-profile.html")
        create_user(username)
        session["username"] = username
        return redirect(url_for("main_menu"))

    return render_template("create-profile.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO: handle errors, and show them to the user
        username = request.form["username"]
        login_user(username)
        session["username"] = username
        return redirect(url_for("main_menu"))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("username")
    return redirect(url_for("start_menu"))

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")

@app.route('/game')
def game():
    # TODO: create a save file, possibly overwriting
    #  the existing save file
    return render_template("game.html")


if __name__ == '__main__':
    app.run(debug=True)

