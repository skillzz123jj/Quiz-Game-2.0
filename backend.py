from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS
from wikidataConnection import get_country_info, get_question_pair
from handleUsers import create_user, user_exists, user_has_savefile
import DatabaseConnector
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'60b676f51c4358745dae296b0e13f16261076c508030a35a3d3c58ebb0717fc8'

#Javascript is able to interact with this function
@app.route('/api/country')
def country_info():
    if not session.get("username"):
        return {"error": "Please log in"}, 403

    country_name = request.args.get('name')
    if not country_name:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        result = get_question_pair(country_name, 'capital')
        if not result:
            return jsonify({'error': 'No data found for the specified country'}), 404
        return jsonify(result)
    except Exception as e:
        print(f"Error in /api/country: {e}")
        return jsonify({'error': 'Failed to retrieve country info'}), 500


@app.route('/createUser')
def handle_create_user():
    username = request.args.get('name')
    if not username:
        return jsonify({'error': 'Missing parameters'}), 400
    create_user(username)
    session["username"] = username
    return jsonify({'message': 'User created successfully'})

@app.route('/')
def start_menu():
    return render_template("start-menu.html")

@app.route('/main-menu')
def main_menu():
    username = session.get("username")
    if not username:
        return redirect(url_for("start_menu"))

    has_savefile = user_has_savefile(username)

    return render_template(
        "main-menu.html",
        username=username,
        has_savefile=has_savefile
    )


@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        username = request.form["username"]
        if not username:
            return render_template(
                "create-profile.html", error="Username is required"
            ), 401
        if user_exists(username):
            return render_template(
                "create-profile.html", error="Username has already been taken"
            ), 403

        create_user(username)
        session["username"] = username
        return redirect(url_for("main_menu"))

    return render_template("create-profile.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        if not username:
            return render_template("login.html", error="Username is required"), 401
        if not user_exists(username):
            return render_template("login.html", error="Invalid username"), 403

        session["username"] = username
        return redirect(url_for("main_menu"))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("username")
    return redirect(url_for("start_menu"))

@app.route('/leaderboard')
def leaderboard():
    return render_template(
        "leaderboard.html",
        username=session.get("username")
    )

@app.route('/game')
def game():
    if not session.get("username"):
        return redirect(url_for("start_menu"))
    # TODO: create a save file, possibly overwriting
    #  the existing save file
    return render_template("game.html")

@app.route('/fetchLives')
def interact_lives():
    username = session.get("username")
    if not username:
        return jsonify({'error': 'User has not logged in'}), 400

    # Get user_id from username (using parameterized query to prevent SQL injection)
    user_query = "SELECT user_id FROM users WHERE username = %s"
    user_result = DatabaseConnector.execute_query(DatabaseConnector.connection, user_query, (username,))

    if not user_result:
        return jsonify({'error': 'User not found'}), 404

    user_id = user_result[0][0]

    #Now get the game_state
    game_query = "SELECT game_state FROM game_progress WHERE user_id = %s"
    game_result = DatabaseConnector.execute_query(DatabaseConnector.connection, game_query, (user_id,))

    if not game_result:
        return jsonify({'error': 'No game progress found'}), 404

    game_state_str = game_result[0][0]

    try:
        game_state = json.loads(game_state_str)
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid game state data'}), 500

    return jsonify({'lives': game_state['lives']})

@app.route('/updateLives', methods=['POST'])
def update_lives():
    username = session.get("username")
    if not username:
        return jsonify({'error': 'User not logged in'}), 400

    data = request.get_json()
    if not data or 'lives' not in data:
        return jsonify({'error': 'Missing lives parameter'}), 400

    new_lives = data['lives']

    #Get user_id from username
    user_query = "SELECT user_id FROM users WHERE username = %s"
    user_result = DatabaseConnector.execute_query(DatabaseConnector.connection, user_query, (username,))
    if not user_result:
        return jsonify({'error': 'User not found'}), 404
    user_id = user_result[0][0]

    #Get current game_state
    game_query = "SELECT game_state FROM game_progress WHERE user_id = %s"
    game_result = DatabaseConnector.execute_query(DatabaseConnector.connection, game_query, (user_id,))
    if not game_result:
        return jsonify({'error': 'No game progress found'}), 404

    try:
        game_state = json.loads(game_result[0][0])
        game_state['lives'] = new_lives
        new_state_str = json.dumps(game_state)

        #Update the game_state in DB
        update_query = "UPDATE game_progress SET game_state = %s WHERE user_id = %s"
        DatabaseConnector.execute_query(DatabaseConnector.connection, update_query, (new_state_str, user_id))

        return jsonify({'message': 'Lives updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/updateJSON', methods=['POST'])
def update_score_and_countries():
    username = session.get("username")
    if not username:
        return jsonify({'error': 'User not logged in'}), 400

    data = request.get_json()
    if not data or 'score' not in data or 'new_country' not in data:
        return jsonify({'error': 'Missing score or new_country parameter'}), 400

    new_score = data['score']
    new_country = data['new_country']

    user_query = "SELECT user_id FROM users WHERE username = %s"
    user_result = DatabaseConnector.execute_query(DatabaseConnector.connection, user_query, (username,))
    if not user_result:
        return jsonify({'error': 'User not found'}), 404
    user_id = user_result[0][0]

    game_query = "SELECT game_state FROM game_progress WHERE user_id = %s"
    game_result = DatabaseConnector.execute_query(DatabaseConnector.connection, game_query, (user_id,))
    if not game_result:
        return jsonify({'error': 'No game progress found'}), 404

    try:
        game_state = json.loads(game_result[0][0])
        game_state['score'] = new_score

        if 'countries' not in game_state:
            game_state['countries'] = []

        if new_country not in game_state['countries']:
            game_state['countries'].append(new_country)

        new_state_str = json.dumps(game_state)

        update_query = "UPDATE game_progress SET game_state = %s WHERE user_id = %s"
        DatabaseConnector.execute_query(DatabaseConnector.connection, update_query, (new_state_str, user_id))

        return jsonify({'message': 'Score and country updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

