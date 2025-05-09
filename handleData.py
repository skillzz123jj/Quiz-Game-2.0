import json
import DatabaseConnector


#These are helper functions to run queries in MariaDB via backend.py

def create_users_table():
    query = """
     CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
    """
    DatabaseConnector.execute_query(DatabaseConnector.connection, query)


def create_scores_table():
    query = """
    CREATE TABLE IF NOT EXISTS completed_games (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        final_score INT NOT NULL,
        ended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """
    DatabaseConnector.execute_query(DatabaseConnector.connection, query)


def save_final_score_and_reset(user_id, final_score):
    try:
        create_scores_table()
        insert_query = """
        INSERT INTO completed_games (user_id, final_score)
        VALUES (%s, %s)
        """
        DatabaseConnector.execute_query(DatabaseConnector.connection, insert_query, (user_id, final_score))

        reset_query = """
        UPDATE game_progress
        SET game_state = '{"lives": 3, "score": 0, "countries": []}',
        game_started = FALSE
        WHERE user_id = %s
        """
        DatabaseConnector.execute_query(DatabaseConnector.connection, reset_query, (user_id,))

        print(f"Final score saved and progress reset for user_id: {user_id}")
        return True

    except Exception as e:
        print(f"Error in save_final_score_and_reset: {e}")
        return False


def create_user(username):
    create_users_table()

    query = "INSERT INTO users (username) VALUE (%s)"
    params = (username,)
    try:
        DatabaseConnector.execute_query(DatabaseConnector.connection, query, params)
        print(f"User '{username}' inserted.")
    except Exception as e:
        print(f"Error inserting user: {e}")
        return

    query = "SELECT user_id FROM users WHERE username = %s"
    result = DatabaseConnector.fetch_one(DatabaseConnector.connection, query, params)
    print(f"Fetch result: {result}")

    if result:
        user_id = result[0]
        create_savefile(user_id)
    else:
        print("No user_id found, skipping savefile.")


def user_exists(username):
    create_users_table()
    query = "SELECT user_id FROM users WHERE username = %s"
    params = (username,)  # Adding parameters this way makes sure that querys are safe
    result = DatabaseConnector.fetch_one(DatabaseConnector.connection, query, params)
    return result is not None


def create_savefile(user_id):
    try:
        query = """
        CREATE TABLE IF NOT EXISTS game_progress(
            user_id INT PRIMARY KEY,
            game_state JSON NOT NULL,
            game_started BOOLEAN DEFAULT FALSE,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        );
        """
        DatabaseConnector.execute_query(DatabaseConnector.connection, query)

        query = """
        INSERT INTO game_progress(user_id, game_state, game_started)
        VALUES(%s, '{"lives": 3, "score": 0, "countries": []}', False);
        """
        params = (user_id,)
        DatabaseConnector.execute_query(DatabaseConnector.connection, query, params)
    except Exception as e:
        print(f"Error creating savefile: {e}")


def check_game_progress(user_id):
    try:
        query = """
        SELECT game_state
        FROM game_progress
        WHERE user_id = %s AND game_started = TRUE;
        """
        params = (user_id,)
        result = DatabaseConnector.fetch_one(DatabaseConnector.connection, query, params)

        if result:
            data = result[0]
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            return json.loads(data)
        else:
            print("No active game found or game not started.")
            return None
    except Exception as e:
        print(f"Error checking game progress: {e}")
        return None


def user_has_savefile(username):
    try:
        query = "SELECT user_id FROM users WHERE username = %s;"
        params = (username,)
        result = DatabaseConnector.fetch_one(DatabaseConnector.connection, query, params)

        if result:
            user_id = result[0]
            game_state = check_game_progress(user_id)
            return game_state is not None
        else:
            return False
    except Exception as e:
        print(f"Error in user_has_savefile: {e}")
        return False


def reset_game_progress(user_id):
    try:
        query = """
        INSERT INTO game_progress (user_id, game_state, game_started)
        VALUES (%s, '{"lives": 3, "score": 0, "countries": []}', TRUE)
        ON DUPLICATE KEY UPDATE
            game_state = VALUES(game_state),
            game_started = VALUES(game_started),
            last_updated = CURRENT_TIMESTAMP;
        """
        params = (user_id,)
        DatabaseConnector.execute_query(DatabaseConnector.connection, query, params)
        print(f"Game progress for user_id {user_id} has been reset or inserted.")
    except Exception as e:
        print(f"Error resetting game progress: {e}")


def get_user_id(username):
    query = "SELECT user_id FROM users WHERE username = %s"
    params = (username,)
    result = DatabaseConnector.fetch_one(DatabaseConnector.connection, query, params)
    return result[0] if result else None


def update_game_progress(user_id, game_state):
    try:
        game_state_str = json.dumps(game_state)
        query = """
        UPDATE game_progress SET game_state = %s WHERE user_id = %s
        """
        params = (game_state_str, user_id)
        DatabaseConnector.execute_query(DatabaseConnector.connection, query, params)
    except Exception as e:
        print(f"Error updating game progress: {e}")


def get_leaderboard_data():
    query = """
    SELECT u.username, c.final_score AS top_score
    FROM completed_games c
    JOIN users u ON c.user_id = u.user_id
    ORDER BY c.final_score DESC
    LIMIT 10
    """
    results = DatabaseConnector.execute_query(DatabaseConnector.connection, query)
    leaderboard = [{'username': row[0], 'score': row[1]} for row in results]
    return leaderboard


def get_game_state_for_user(user_id):
    query = "SELECT game_state FROM game_progress WHERE user_id = %s"
    result = DatabaseConnector.execute_query(DatabaseConnector.connection, query, (user_id,))
    if not result:
        raise ValueError('No game progress found')

    try:
        game_state = json.loads(result[0][0])
        return game_state
    except json.JSONDecodeError:
        raise ValueError('Invalid game state data')


def update_game_state(user_id, game_state):
    new_state_str = json.dumps(game_state)
    update_query = "UPDATE game_progress SET game_state = %s WHERE user_id = %s"
    DatabaseConnector.execute_query(DatabaseConnector.connection, update_query, (new_state_str, user_id))
