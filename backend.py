from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS

from handleData import create_user, user_exists, user_has_savefile, reset_game_progress, get_user_id, \
    check_game_progress, save_final_score_and_reset, get_leaderboard_data, get_game_state_for_user,  \
    update_game_state
from wikidataConnection import get_question_pair

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'60b676f51c4358745dae296b0e13f16261076c508030a35a3d3c58ebb0717fc8'


# Javascript is able to interact with these functions
@app.route('/api/country')
def country_info():
    if not session.get("username"):
        return {"error": "Please log in"}, 403

    country_name = request.args.get('name')
    if not country_name:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        result = get_question_pair(country_name)
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


#Opens the leaderboard
@app.route('/leaderboard')
def leaderboard():
    return render_template(
        "leaderboard.html",
        username=session.get("username")
    )

#Opens the game and resets progress if player starts a new save
@app.route('/game')
def game():
    if not session.get("username"):
        return redirect(url_for("start_menu"))

    action = request.args.get("action")
    username = session.get("username")

    user_id = get_user_id(username)  # Make sure this fetches valid ID

    if action == "new":
        reset_game_progress(user_id)
    elif action == "load":
        pass

    game_state = check_game_progress(user_id)

    if not game_state:
        game_state = {"lives": 3, "score": 0, "countries": []}

    return render_template("game.html", game_state=game_state)

#Fetches players remaining lives from database to see how many they have left
@app.route('/fetchLives')
def lower_lives():
    username = session.get("username")
    if not username:
        return jsonify({'error': 'User has not logged in'}), 400

    try:
        user_id = get_user_id(username)
        if not user_id:
            return jsonify({'error': 'User not found'}), 404

        game_state = get_game_state_for_user(user_id)
        return jsonify({'lives': game_state['lives']})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Updates lost lives to database upon player losing a life
@app.route('/updateLives', methods=['POST'])
def update_lives():
    username = session.get("username")
    if not username:
        return jsonify({'error': 'User not logged in'}), 400

    data = request.get_json()
    if not data or 'lives' not in data:
        return jsonify({'error': 'Missing lives parameter'}), 400

    new_lives = data['lives']

    try:
        user_id = get_user_id(username)
        if not user_id:
            return jsonify({'error': 'User not found'}), 404

        game_state = get_game_state_for_user(user_id)
        game_state['lives'] = new_lives

        update_game_state(user_id, game_state)

        return jsonify({'message': 'Lives updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Updates score and collected countries to database in realtime
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

        try:
            user_id = get_user_id(username)
            if not user_id:
                return jsonify({'error': 'User not found'}), 404

            game_state = get_game_state_for_user(user_id)
            game_state['score'] = new_score

            if 'countries' not in game_state:
                game_state['countries'] = []

            if new_country not in game_state['countries']:
                game_state['countries'].append(new_country)

            update_game_state(user_id, game_state)

            return jsonify({'message': 'Score and country updated successfully'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500


#When the game ends this saves players score and resets savefile
@app.route('/endGame', methods=['POST'])
def end_game():
    try:
        username = session.get('username')
        if not username:
            return jsonify({'error': 'User not logged in'}), 400

        data = request.get_json()
        final_score = data.get('score')

        user_id = get_user_id(username)
        if user_id is None or final_score is None:
            return jsonify({'error': 'Missing user ID or score'}), 400

        success = save_final_score_and_reset(user_id, final_score)
        if not success:
            return jsonify({'error': 'Could not save game data'}), 500

        return jsonify({'message': 'Game ended and data saved'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Fetches leaderboard data
@app.route('/getLeaderboard', methods=['GET'])
def get_leaderboard():
        try:
            leaderboard = get_leaderboard_data()
            return jsonify(leaderboard)
        except Exception as e:
            return jsonify({'error': str(e)}), 500


#Fetches countries to see which ones player has collected upon game load
@app.route('/get-countries')
def completed_countries():
        username = session.get("username")
        if not username:
            return jsonify({'error': 'User not logged in'}), 400

        user_id = get_user_id(username)

        try:
            game_state = get_game_state_for_user(user_id)
            countries = game_state.get('countries', [])
            return jsonify({'countries': countries})
        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
